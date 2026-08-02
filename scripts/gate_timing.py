#!/usr/bin/env python3
"""Gate timing harness — machine stage clocks + human gate wait slots.

Contract: gate-timing.v1
Human waits are recorded separately from machine work so Gate 1/2/3 latency
can be measured in real sessions without inventing LLM times.

Usage:
  python3 scripts/gate_timing.py human --scenario token-refresh \\
      --gate1-sec 90 --gate2-sec 75 --gate3-sec 45 --reviewer "qa-reviewer"
  python3 scripts/gate_timing.py human --scenario duplicate --interactive
  python3 scripts/gate_timing.py summarize
  python3 scripts/gate_timing.py smoke
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from patch_pipeline import propose as propose_recipe  # noqa: E402
from tools_runner import invoke as tools_invoke  # noqa: E402
from workflow_runner import (  # noqa: E402
    build_analysis,
    build_plan,
    collect_context,
)

METRICS_DIR = ROOT / ".forgeone/runs/metrics"
HUMAN_LOG_DIR = ROOT / "docs/ai-evolution/evals/human-sessions"
BASELINE_PATH = ROOT / "docs/ai-evolution/evals/gate-timing-baseline.json"
CONTRACT = "gate-timing.v1"

SCENARIOS: dict[str, dict[str, Any]] = {
    "duplicate": {
        "request_id": "AUTH-DUPLICATE-BUILDER",
        "terms": "LoginRequestBuilder",
        "target": "csharp",
        "domain": "Auth",
        "recipe": "good-access-token-expired",
        "expect_already_covered": True,
        "checklist": [
            "Gate1: confirmar analysis already_covered / evidence LoginRequestBuilder",
            "Gate2: plan reuse builders incluye LoginRequestBuilder; create=[]",
            "Gate3: N/A (no propose) — anotar 0",
        ],
    },
    "token-refresh": {
        "request_id": "AUTH-TOKEN-REFRESH",
        "terms": "TokenRefresh access token",
        "target": "csharp",
        "domain": "Auth",
        "recipe": "good-access-token-expired",
        "expect_already_covered": False,
        "checklist": [
            "Gate1: leer summary + evidence de FakeAuthApi / TokenRefresh",
            "Gate2: reuse vs create_only_if_needed; searched_before_create",
            "Gate3: proposal awaiting_gate3; review clean; NO apply en la sesión de medición",
        ],
    },
    "login-neg": {
        "request_id": "AUTH-LOGIN-NEG",
        "terms": "invalid login credentials",
        "target": "csharp",
        "domain": "Auth",
        "recipe": None,
        "expect_already_covered": True,
        "checklist": [
            "Gate1: coverage ya existe (Login.feature / LoginSteps)",
            "Gate2: already_covered → no crear Feature gemela",
            "Gate3: N/A — anotar 0",
        ],
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]


def timed(fn):  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    value = fn()
    ms = round((time.perf_counter() - start) * 1000, 1)
    return value, ms


def parse_duration_to_ms(raw: str) -> int:
    """Accept 90, 90s, 1.5m, 2m, 1:30 → milliseconds."""
    text = raw.strip().lower()
    if not text:
        return 0
    if re.fullmatch(r"\d+:\d{1,2}", text):
        minutes, seconds = text.split(":")
        return (int(minutes) * 60 + int(seconds)) * 1000
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(ms|s|m|sec|secs|min|mins)?", text)
    if not m:
        raise ValueError(f"Bad duration {raw!r}; use 90, 90s, 2m, or 1:30")
    value = float(m.group(1))
    unit = m.group(2) or "s"
    if unit == "ms":
        return int(value)
    if unit in ("s", "sec", "secs"):
        return int(value * 1000)
    if unit in ("m", "min", "mins"):
        return int(value * 60_000)
    return int(value * 1000)


def save_session(session: dict[str, Any]) -> Path:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    path = METRICS_DIR / f"{session['session_id']}.json"
    path.write_text(json.dumps(session, indent=2), encoding="utf-8")
    return path


def write_review_artifacts(session_id: str, analysis: dict[str, Any], plan: dict[str, Any]) -> Path:
    """Drop YAML-ish JSON for the human to read at Gate 1/2 (no extra deps)."""
    out = METRICS_DIR / session_id
    out.mkdir(parents=True, exist_ok=True)
    (out / "analysis.v1.json").write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    (out / "plan.v1.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return out


def run_session(
    request_id: str,
    terms: str,
    target: str,
    domain: str,
    recipe: str | None,
    gate1_ms: int,
    gate2_ms: int,
    gate3_ms: int,
    auto_gates: bool,
    note: str,
    *,
    reviewer: str = "",
    scenario: str = "",
    write_artifacts: bool = False,
) -> dict[str, Any]:
    session_id = new_id()
    stages: list[dict[str, Any]] = []

    def add(name: str, ms: float, detail: dict[str, Any] | None = None) -> None:
        stages.append({"name": name, "elapsed_ms": ms, **(detail or {})})

    req = {
        "request_id": request_id,
        "terms": terms,
        "target": target,
        "domain": domain,
        "description": f"gate_timing harness for {request_id}",
        "constraints": "",
    }

    (ctx, context_ms) = timed(lambda: collect_context(target, terms, request_id))
    tools_invoked, evidence, buckets = ctx
    add("context", context_ms, {"tools": [t.get("tool") for t in tools_invoked] if tools_invoked else []})

    (analysis, analysis_ms) = timed(lambda: build_analysis(req, evidence, buckets))
    add("analysis", analysis_ms, {"already_covered": bool(analysis.get("meta", {}).get("already_covered"))})

    if auto_gates:
        add("gate1_human", float(gate1_ms), {"mode": "recorded_or_zero", "decision": "approved"})
    else:
        add("gate1_human", float(gate1_ms), {"mode": "pending_human", "decision": "pending"})

    (plan, plan_ms) = timed(lambda: build_plan(req, analysis, evidence, buckets))
    add("plan", plan_ms, {"already_covered": bool(plan.get("meta", {}).get("already_covered"))})

    if auto_gates:
        add("gate2_human", float(gate2_ms), {"mode": "recorded_or_zero", "decision": "approved"})
    else:
        add("gate2_human", float(gate2_ms), {"mode": "pending_human", "decision": "pending"})

    propose_status = None
    proposal_id = None
    if recipe and not plan.get("meta", {}).get("already_covered"):
        (proposal, propose_ms) = timed(lambda: propose_recipe(recipe, None, "gate_timing"))
        propose_status = proposal.get("status")
        proposal_id = proposal.get("proposal_id")
        add(
            "propose",
            propose_ms,
            {"recipe": recipe, "status": propose_status, "proposal_id": proposal_id},
        )
        add("gate3_human", float(gate3_ms), {"mode": "recorded_or_zero_no_apply", "applied": False})
    elif recipe and plan.get("meta", {}).get("already_covered"):
        add("propose", 0.0, {"skipped": True, "reason": "already_covered", "recipe": recipe})
        add("gate3_human", 0.0, {"skipped": True})
    else:
        add("propose", 0.0, {"skipped": True, "reason": "no_recipe"})
        add("gate3_human", 0.0, {"skipped": True, "reason": "no_recipe"})

    machine_ms = round(sum(s["elapsed_ms"] for s in stages if not s["name"].endswith("_human")), 1)
    human_ms = round(sum(s["elapsed_ms"] for s in stages if s["name"].endswith("_human")), 1)

    artifacts_dir = None
    if write_artifacts:
        artifacts_dir = str(write_review_artifacts(session_id, analysis, plan).relative_to(ROOT))

    session = {
        "contract": CONTRACT,
        "session_id": session_id,
        "timestamp": utc_now(),
        "request_id": request_id,
        "terms": terms,
        "target": target,
        "domain": domain,
        "scenario": scenario or None,
        "reviewer": reviewer or None,
        "auto_gates": auto_gates,
        "note": note,
        "stages": stages,
        "totals": {
            "machine_ms": machine_ms,
            "human_gate_ms": human_ms,
            "wall_ms": round(machine_ms + human_ms, 1),
        },
        "artifacts": {
            "evidence_count": len(evidence),
            "already_covered": bool(plan.get("meta", {}).get("already_covered")),
            "proposal_id": proposal_id,
            "propose_status": propose_status,
            "review_bundle": artifacts_dir,
        },
        "producer": "scripts/gate_timing.py",
    }
    path = save_session(session)
    session["path"] = str(path.relative_to(ROOT))
    return session


def record_human_waits(
    session_file: Path,
    gate1_ms: int | None,
    gate2_ms: int | None,
    gate3_ms: int | None,
    note: str,
) -> dict[str, Any]:
    session = json.loads(session_file.read_text(encoding="utf-8"))
    updates = {
        "gate1_human": gate1_ms,
        "gate2_human": gate2_ms,
        "gate3_human": gate3_ms,
    }
    for stage in session["stages"]:
        name = stage["name"]
        if name in updates and updates[name] is not None:
            stage["elapsed_ms"] = float(updates[name])
            stage["mode"] = "human_recorded"
    machine_ms = round(sum(s["elapsed_ms"] for s in session["stages"] if not s["name"].endswith("_human")), 1)
    human_ms = round(sum(s["elapsed_ms"] for s in session["stages"] if s["name"].endswith("_human")), 1)
    session["totals"] = {
        "machine_ms": machine_ms,
        "human_gate_ms": human_ms,
        "wall_ms": round(machine_ms + human_ms, 1),
    }
    if note:
        session["note"] = (session.get("note") or "") + f" | {note}"
    session["updated_at"] = utc_now()
    session_file.write_text(json.dumps(session, indent=2), encoding="utf-8")
    return session


def write_human_markdown(session: dict[str, Any], checklist: list[str]) -> Path:
    HUMAN_LOG_DIR.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sid = session["session_id"]
    path = HUMAN_LOG_DIR / f"{day}-{sid}.md"
    t = session["totals"]
    gates = {s["name"]: s["elapsed_ms"] for s in session["stages"] if s["name"].endswith("_human")}
    lines = [
        f"# Human gate session — {session.get('scenario') or session['request_id']}",
        "",
        f"- **session_id:** `{sid}`",
        f"- **request_id:** `{session['request_id']}`",
        f"- **reviewer:** {session.get('reviewer') or '(anon)'}",
        f"- **timestamp:** {session['timestamp']}",
        f"- **note:** {session.get('note') or ''}",
        f"- **json:** `{session['path']}`",
        "",
        "## Totals",
        "",
        f"| machine_ms | human_gate_ms | wall_ms |",
        f"|------------|---------------|---------|",
        f"| {t['machine_ms']} | {t['human_gate_ms']} | {t['wall_ms']} |",
        "",
        "## Human gates (ms)",
        "",
        f"| Gate 1 | Gate 2 | Gate 3 |",
        f"|--------|--------|--------|",
        f"| {gates.get('gate1_human', 0)} | {gates.get('gate2_human', 0)} | {gates.get('gate3_human', 0)} |",
        "",
        "## Checklist",
        "",
    ]
    for item in checklist:
        lines.append(f"- [x] {item}")
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- already_covered: `{session['artifacts'].get('already_covered')}`",
            f"- proposal_id: `{session['artifacts'].get('proposal_id')}`",
            f"- propose_status: `{session['artifacts'].get('propose_status')}`",
            f"- review_bundle: `{session['artifacts'].get('review_bundle')}`",
            "",
            "> Apply was **not** part of this measurement (Gate 3 = read/decide only).",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def prompt_duration(label: str, default_sec: str = "0") -> int:
    raw = input(f"{label} [{default_sec}s / 1:30 / 2m]: ").strip() or default_sec
    return parse_duration_to_ms(raw)


def cmd_human(args: argparse.Namespace) -> int:
    if args.scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario {args.scenario!r}; choose from {sorted(SCENARIOS)}")
    spec = SCENARIOS[args.scenario]

    print(f"# human session scenario={args.scenario} request_id={spec['request_id']}")
    print("# checklist:")
    for item in spec["checklist"]:
        print(f"  - {item}")

    # Machine first (human clocks start when reading artifacts)
    session = run_session(
        request_id=spec["request_id"],
        terms=spec["terms"],
        target=spec["target"],
        domain=spec["domain"],
        recipe=spec.get("recipe"),
        gate1_ms=0,
        gate2_ms=0,
        gate3_ms=0,
        auto_gates=True,
        note=args.note or f"human scenario={args.scenario}",
        reviewer=args.reviewer,
        scenario=args.scenario,
        write_artifacts=True,
    )
    print(f"# machine done machine_ms={session['totals']['machine_ms']}")
    print(f"# review bundle: {session['artifacts'].get('review_bundle')}")
    print(f"# session json: {session['path']}")

    if args.interactive:
        print("# Start your stopwatch when you open analysis.v1.json")
        g1 = prompt_duration("Gate1 read+decide")
        g2 = prompt_duration("Gate2 read+decide")
        if session["artifacts"].get("propose_status") or (
            not session["artifacts"].get("already_covered") and spec.get("recipe")
        ):
            g3 = prompt_duration("Gate3 read proposal (no apply)", "0")
        else:
            print("# Gate3 skipped (already_covered / no proposal)")
            g3 = 0
    else:

        def gate_ms(duration: str | None, sec: float | None) -> int:
            if duration is not None:
                return parse_duration_to_ms(duration)
            if sec is not None:
                return int(sec * 1000)
            return 0

        g1 = gate_ms(args.gate1, args.gate1_sec)
        g2 = gate_ms(args.gate2, args.gate2_sec)
        g3 = gate_ms(args.gate3, args.gate3_sec)

    session_rel = session["path"]
    session = record_human_waits(
        ROOT / session_rel,
        gate1_ms=g1,
        gate2_ms=g2,
        gate3_ms=g3,
        note="human_recorded",
    )
    session["path"] = session_rel
    if args.reviewer:
        session["reviewer"] = args.reviewer
        (ROOT / session_rel).write_text(json.dumps(session, indent=2), encoding="utf-8")

    md = write_human_markdown(session, spec["checklist"])
    t = session["totals"]
    print(
        f"# human_gate_ms={t['human_gate_ms']} wall_ms={t['wall_ms']} "
        f"log={md.relative_to(ROOT)}"
    )
    if args.json:
        print(json.dumps(session, indent=2))
    return 0


def cmd_summarize() -> int:
    files = sorted(METRICS_DIR.glob("*.json")) if METRICS_DIR.is_dir() else []
    humanish = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("contract") != CONTRACT:
            continue
        # Prefer sessions with recorded human time or reviewer/scenario
        human_ms = float(data.get("totals", {}).get("human_gate_ms") or 0)
        if human_ms > 0 or data.get("reviewer") or data.get("scenario"):
            humanish.append(data)

    print(f"# gate_timing summarize sessions={len(humanish)} (of {len(files)} metrics files)")
    if not humanish:
        print("# no human-recorded sessions yet — run: gate_timing.py human --scenario duplicate --gate1-sec 60 …")
        return 0

    by_scenario: dict[str, list[dict[str, Any]]] = {}
    for s in humanish:
        key = s.get("scenario") or s.get("request_id") or "unknown"
        by_scenario.setdefault(str(key), []).append(s)

    for key, items in sorted(by_scenario.items()):
        n = len(items)
        avg_h = round(sum(i["totals"]["human_gate_ms"] for i in items) / n, 1)
        avg_m = round(sum(i["totals"]["machine_ms"] for i in items) / n, 1)
        avg_w = round(sum(i["totals"]["wall_ms"] for i in items) / n, 1)
        print(f"- {key}: n={n} avg_machine_ms={avg_m} avg_human_ms={avg_h} avg_wall_ms={avg_w}")
    return 0


def cmd_smoke() -> int:
    checks: list[tuple[str, bool, str]] = []

    dup = run_session(
        request_id="AUTH-DUPLICATE-BUILDER",
        terms="LoginRequestBuilder",
        target="csharp",
        domain="Auth",
        recipe="good-access-token-expired",
        gate1_ms=0,
        gate2_ms=0,
        gate3_ms=0,
        auto_gates=True,
        note="smoke: already_covered skip propose",
        scenario="duplicate",
    )
    ok_dup = (
        dup["contract"] == CONTRACT
        and dup["artifacts"]["already_covered"] is True
        and any(s["name"] == "propose" and s.get("skipped") for s in dup["stages"])
        and dup["totals"]["machine_ms"] >= 0
    )
    checks.append(("duplicate_skip_propose", ok_dup, dup["session_id"]))

    good = run_session(
        request_id="AUTH-TOKEN-REFRESH",
        terms="TokenRefresh access token",
        target="csharp",
        domain="Auth",
        recipe="good-access-token-expired",
        gate1_ms=0,
        gate2_ms=0,
        gate3_ms=0,
        auto_gates=True,
        note="smoke: propose awaiting_gate3",
        scenario="token-refresh",
        write_artifacts=True,
    )
    propose_stage = next(s for s in good["stages"] if s["name"] == "propose")
    ok_good = propose_stage.get("status") == "awaiting_gate3" and not propose_stage.get("skipped")
    checks.append(("token_propose_awaiting_gate3", ok_good, str(propose_stage.get("proposal_id"))))

    path = ROOT / good["path"]
    updated = record_human_waits(path, gate1_ms=120000, gate2_ms=60000, gate3_ms=30000, note="smoke human fills")
    ok_human = updated["totals"]["human_gate_ms"] == 210000.0
    checks.append(("record_human_waits", ok_human, str(updated["totals"]["human_gate_ms"])))

    listed, list_ms = timed(
        lambda: tools_invoke(
            "find_existing_builder",
            {"target": "csharp", "terms": "LoginRequestBuilder", "limit": "3"},
            no_audit=True,
        )
    )
    ok_tool = bool(listed.get("ok")) and list_ms >= 0
    checks.append(("tools_runner_reachable", ok_tool, f"{list_ms}ms"))

    # Non-interactive human path + markdown log
    ns = argparse.Namespace(
        scenario="duplicate",
        reviewer="smoke-bot",
        note="smoke human path",
        interactive=False,
        gate1=None,
        gate2=None,
        gate3=None,
        gate1_sec=45,
        gate2_sec=30,
        gate3_sec=0,
        json=False,
    )
    rc = cmd_human(ns)
    ok_human_cmd = rc == 0 and any(
        "smoke-bot" in p.read_text(encoding="utf-8") for p in HUMAN_LOG_DIR.glob("*.md")
    )
    checks.append(("human_command_log", ok_human_cmd, f"rc={rc} logs={len(list(HUMAN_LOG_DIR.glob('*.md')))}"))

    ok_parse = parse_duration_to_ms("1:30") == 90_000 and parse_duration_to_ms("2m") == 120_000
    checks.append(("parse_duration", ok_parse, "1:30 / 2m"))

    baseline = {
        "contract": CONTRACT,
        "updated": utc_now(),
        "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
        "sample_session_ids": [dup["session_id"], good["session_id"]],
        "scenarios": sorted(SCENARIOS),
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2), encoding="utf-8")

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# gate_timing smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    print(f"# baseline={BASELINE_PATH.relative_to(ROOT)}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Time machine stages (+ optional human ms)")
    run.add_argument("--request-id", required=True)
    run.add_argument("--terms", required=True)
    run.add_argument("--target", default="csharp", choices=["csharp", "python"])
    run.add_argument("--domain", default="Auth")
    run.add_argument("--recipe", default=None)
    run.add_argument("--gate1-ms", type=int, default=0)
    run.add_argument("--gate2-ms", type=int, default=0)
    run.add_argument("--gate3-ms", type=int, default=0)
    run.add_argument("--auto-gates", action="store_true")
    run.add_argument("--note", default="")
    run.add_argument("--json", action="store_true")

    rec = sub.add_parser("record", help="Fill human gate waits on an existing session JSON")
    rec.add_argument("--session-file", required=True)
    rec.add_argument("--gate1-ms", type=int, default=None)
    rec.add_argument("--gate2-ms", type=int, default=None)
    rec.add_argument("--gate3-ms", type=int, default=None)
    rec.add_argument("--note", default="")
    rec.add_argument("--json", action="store_true")

    hum = sub.add_parser("human", help="Guided human gate measurement for a known scenario")
    hum.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    hum.add_argument("--reviewer", default="")
    hum.add_argument("--note", default="")
    hum.add_argument("--interactive", action="store_true")
    hum.add_argument("--gate1", default=None, help="Duration e.g. 90s / 1:30 / 2m")
    hum.add_argument("--gate2", default=None)
    hum.add_argument("--gate3", default=None)
    hum.add_argument("--gate1-sec", type=float, default=None)
    hum.add_argument("--gate2-sec", type=float, default=None)
    hum.add_argument("--gate3-sec", type=float, default=None)
    hum.add_argument("--json", action="store_true")

    sub.add_parser("summarize", help="Average human/machine times from metrics sessions")
    sub.add_parser("smoke", help="Deterministic smoke for gate-timing.v1")
    sub.add_parser("scenarios", help="List human scenarios")

    args = parser.parse_args()
    try:
        if args.command == "run":
            session = run_session(
                request_id=args.request_id,
                terms=args.terms,
                target=args.target,
                domain=args.domain,
                recipe=args.recipe,
                gate1_ms=args.gate1_ms,
                gate2_ms=args.gate2_ms,
                gate3_ms=args.gate3_ms,
                auto_gates=args.auto_gates,
                note=args.note,
            )
            if args.json:
                print(json.dumps(session, indent=2))
            else:
                t = session["totals"]
                print(
                    f"# session_id={session['session_id']} "
                    f"machine_ms={t['machine_ms']} human_gate_ms={t['human_gate_ms']} wall_ms={t['wall_ms']}"
                )
                for stage in session["stages"]:
                    print(f"- {stage['name']}: {stage['elapsed_ms']}ms")
                print(f"# saved={session['path']}")
            return 0
        if args.command == "record":
            session = record_human_waits(
                Path(args.session_file),
                args.gate1_ms,
                args.gate2_ms,
                args.gate3_ms,
                args.note,
            )
            print(
                json.dumps(session, indent=2)
                if args.json
                else f"# updated human_gate_ms={session['totals']['human_gate_ms']}"
            )
            return 0
        if args.command == "human":
            return cmd_human(args)
        if args.command == "summarize":
            return cmd_summarize()
        if args.command == "scenarios":
            for name, spec in SCENARIOS.items():
                print(f"- {name}: {spec['request_id']} recipe={spec.get('recipe')}")
            return 0
        if args.command == "smoke":
            return cmd_smoke()
    except (ValueError, FileNotFoundError, KeyError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
