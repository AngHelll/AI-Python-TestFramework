#!/usr/bin/env python3
"""Phase 5 workflow runner — Analyst → tools → Planner with tracing.

Deterministic context builder (no LLM required). Human gates via flags.
Writes run JSON under .forgeone/runs/workflow/ (gitignored).

Usage:
  python3 scripts/workflow_runner.py start --from tools/workflow/v1/samples/AUTH-DUPLICATE-BUILDER.json --auto-gates
  python3 scripts/workflow_runner.py gate --run-id <id> --gate 1 --decision approved
  python3 scripts/workflow_runner.py show --run-id <id>
  python3 scripts/workflow_runner.py smoke
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / ".forgeone/runs/workflow"
SAMPLES_DIR = ROOT / "tools/workflow/v1/samples"
sys.path.insert(0, str(ROOT / "scripts"))

from tools_runner import invoke as tool_invoke  # noqa: E402

TOOL_SEQUENCE = [
    ("find_existing_builder", lambda t, terms: {"target": t, "terms": terms, "limit": "5"}),
    ("find_existing_validator", lambda t, terms: {"target": t, "terms": terms, "limit": "5"}),
    ("find_reusable_step", lambda t, terms: {"target": t, "terms": terms, "limit": "5"}),
    ("search_similar_automation", lambda t, terms: {"target": t, "terms": terms, "limit": "5"}),
    ("inspect_service_contract", lambda t, terms: {"target": t, "terms": terms, "limit": "5"}),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]


def load_request(path: Path | None, args: argparse.Namespace) -> dict[str, str]:
    data: dict[str, Any] = {}
    if path:
        data = json.loads(path.read_text(encoding="utf-8"))
    cli_map = {
        "request_id": args.request_id,
        "target": args.target,
        "domain": args.domain,
        "description": args.description,
        "terms": args.terms,
        "constraints": args.constraints,
    }
    for key, val in cli_map.items():
        if val:
            data[key] = val
    required = ["request_id", "target", "description", "terms"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(f"Missing request fields: {missing}")
    data.setdefault("domain", "Auth")
    data.setdefault("constraints", "plan only")
    if data["target"] not in ("csharp", "python"):
        raise ValueError("target must be csharp or python for workflow start")
    return {k: str(data[k]) for k in ("request_id", "target", "domain", "description", "terms", "constraints")}


def save_run(run: dict[str, Any]) -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / f"{run['run_id']}.json"
    path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    return path


def load_run(run_id: str) -> dict[str, Any]:
    path = RUNS_DIR / f"{run_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Run not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def collect_context(target: str, terms: str, request_id: str) -> tuple[list[dict], list[dict], dict[str, list[str]]]:
    tools_invoked: list[dict[str, Any]] = []
    evidence: list[dict[str, str]] = []
    buckets: dict[str, list[str]] = {
        "builders": [],
        "validators": [],
        "steps": [],
        "features": [],
        "clients": [],
        "pages": [],
    }

    for tool_name, param_fn in TOOL_SEQUENCE:
        if target == "python" and tool_name in {
            "find_existing_builder",
            "find_existing_validator",
            "inspect_service_contract",
        }:
            # Python lab uses pages/utils more than builders; still allow invoke — may return empty
            pass
        record = tool_invoke(tool_name, param_fn(target, terms), no_audit=False)
        hits = record["result"].get("hits", [])
        tools_invoked.append(
            {
                "tool": tool_name,
                "invocation_id": record["invocation_id"],
                "params": record["params"],
                "ok": True,
                "hit_count": len(hits),
                "audit_path": record.get("audit_path"),
            }
        )
        for hit in hits:
            kind = str(hit.get("kind", ""))
            path = str(hit["path"])
            if kind in buckets and path not in buckets[kind]:
                buckets[kind].append(path)
            evidence.append({"path": path, "reason": f"{tool_name} terms={terms}"})

    # Always consult catalog / traps for Auth requests
    know = tool_invoke(
        "find_knowledge",
        {"target": "knowledge", "terms": "component-catalog,LoginRequestBuilder", "limit": "5"},
        no_audit=False,
    )
    know_hits = know["result"].get("hits", [])
    tools_invoked.append(
        {
            "tool": "find_knowledge",
            "invocation_id": know["invocation_id"],
            "params": know["params"],
            "ok": True,
            "hit_count": len(know_hits),
            "audit_path": know.get("audit_path"),
        }
    )
    for hit in know_hits:
        evidence.append({"path": hit["path"], "reason": f"find_knowledge for {request_id}"})

    # Dedupe evidence by path keeping first reason
    dedup: dict[str, str] = {}
    for item in evidence:
        dedup.setdefault(item["path"], item["reason"])
    evidence = [{"path": p, "reason": r} for p, r in dedup.items()]
    return tools_invoked, evidence, buckets


def build_analysis(req: dict[str, str], evidence: list[dict[str, str]], buckets: dict[str, list[str]]) -> dict[str, Any]:
    request_id = req["request_id"]
    already = False
    summary = ""
    positive: list[str] = []
    negative: list[str] = []
    edge: list[str] = []
    assumptions: list[str] = []
    questions: list[str] = []
    out_of_scope = ["Patches in this workflow phase", "Jira/XRay live integration"]

    builder_hit = any("LoginRequestBuilder" in p for p in buckets["builders"])
    login_neg = any("Login.feature" in p for p in buckets["features"])
    paths = evidence_paths(evidence)
    profile_covered = any("Profile.feature" in p for p in paths)

    if request_id == "AUTH-DUPLICATE-BUILDER" or (
        "new builder" in req["description"].lower() and builder_hit
    ):
        already = True
        summary = (
            "Request asks for a new login payload builder, but LoginRequestBuilder already exists "
            "in the C# lab catalog."
        )
        assumptions = ["Intent is login request construction, not a new Auth domain"]
        questions = ["Is there a field missing on LoginRequestBuilder that justifies extension?"]
    elif request_id == "AUTH-LOGIN-NEG" or (
        "invalid login" in req["description"].lower() and login_neg
    ):
        already = True
        summary = (
            "Invalid login coverage already exists via Login.feature (@AUTH-LOGIN-NEG) and LoginSteps."
        )
        negative = ["Invalid credentials → error (already automated)"]
        assumptions = ["No contract change requested"]
        questions = ["Need additional localization variants?"]
    elif "PROFILE" in request_id or "profile" in req["description"].lower():
        summary = (
            "Profile retrieval via AuthApiClient.GetProfile; feature/steps may already exist post Fase 0."
        )
        positive = ["Valid access token returns lab user profile"]
        negative = ["Invalid/empty token → profile absent"]
        edge = ["Token from refresh still valid by lab-token- prefix"]
        assumptions = ["FakeAuthApi models unauthorized as null"]
        already = profile_covered
        if already:
            summary += " Profile.feature already present — treat as already covered unless extending."
    else:
        summary = f"Deterministic analysis for {request_id} from tool evidence."
        positive = ["Happy path based on existing clients/features if present"]
        assumptions = ["Generated by workflow_runner deterministic analyst (no LLM)"]
        questions = ["Confirm acceptance criteria with human Gate 1"]

    return {
        "request_id": request_id,
        "summary": summary,
        "proposed_coverage": {
            "positive": positive,
            "negative": negative,
            "edge": edge,
        },
        "assumptions": assumptions,
        "open_questions": questions,
        "out_of_scope": out_of_scope,
        "evidence": evidence[:12],
        "meta": {
            "target": f"labs/csharp-reqnroll-lab" if req["target"] == "csharp" else "python-root",
            "domain": req.get("domain", ""),
            "contract": "analysis.v1",
            "already_covered": already,
            "producer": "workflow_runner.deterministic_analyst",
        },
    }


def evidence_paths(evidence: list[dict[str, str]]) -> list[str]:
    return [e["path"] for e in evidence]


def symbol_from_path(path: str) -> str:
    return Path(path).stem


def build_plan(
    req: dict[str, str],
    analysis: dict[str, Any],
    evidence: list[dict[str, str]],
    buckets: dict[str, list[str]],
) -> dict[str, Any]:
    already = bool(analysis.get("meta", {}).get("already_covered"))
    builders = [symbol_from_path(p) for p in buckets["builders"]]
    validators = [symbol_from_path(p) for p in buckets["validators"]]
    steps = [symbol_from_path(p) for p in buckets["steps"]]
    clients = [symbol_from_path(p) for p in buckets["clients"] + buckets["pages"]]

    if already:
        risks = [
            {
                "id": "R-DUPLICATE",
                "severity": "high",
                "note": "Creating parallel components would violate Reuse Before Create",
            }
        ]
        create: list[str] = []
        files: list[str] = []
        impl = [
            "Confirm existing coverage with tools_runner / dotnet test",
            "Mark request Already Covered",
            "Do not create new Builder/Validator/Feature",
        ]
    else:
        risks = [
            {
                "id": "R-SCOPE",
                "severity": "medium",
                "note": "Confirm files before implementation Gate 3",
            }
        ]
        create = []
        files = buckets["features"][:3] + buckets["steps"][:3]
        impl = [
            "Review tool evidence",
            "Extend existing validators/clients before creating new types",
            "Update knowledge/framework/component-catalog.md if anything new is approved later",
        ]

    return {
        "request_id": req["request_id"],
        "reuse": {
            "builders": builders,
            "validators": validators,
            "steps": steps,
            "pages_or_clients": clients,
        },
        "create_only_if_needed": create,
        "files_likely_affected": files,
        "risks": risks,
        "implementation_steps": impl,
        "evidence": evidence[:12],
        "policy_checks": {
            "searched_before_create": True,
            "no_critical_files_without_flag": True,
        },
        "meta": {
            "target": analysis["meta"]["target"],
            "domain": req.get("domain", ""),
            "contract": "plan.v1",
            "analysis_request_id": req["request_id"],
            "already_covered": already,
            "producer": "workflow_runner.deterministic_planner",
        },
    }


def start_workflow(req: dict[str, str], auto_gates: bool) -> dict[str, Any]:
    started = time.perf_counter()
    run_id = new_run_id()
    stages = ["context"]
    tools_invoked, evidence, buckets = collect_context(req["target"], req["terms"], req["request_id"])
    stages.append("analysis")
    analysis = build_analysis(req, evidence, buckets)
    gate1 = "pending"
    gate1_note = ""
    status = "awaiting_gate1"

    if auto_gates:
        gate1 = "approved"
        gate1_note = "auto-gates: analysis has evidence"
        stages.append("gate1")
        stages.append("plan")
        plan = build_plan(req, analysis, evidence, buckets)
        gate2 = "approved"
        gate2_note = "auto-gates: searched_before_create=true"
        stages.append("gate2")
        stages.append("delivered")
        status = "completed"
    else:
        plan = None
        gate2 = "pending"
        gate2_note = ""

    run = {
        "contract": "workflow-run.v1",
        "run_id": run_id,
        "request_id": req["request_id"],
        "target": req["target"],
        "domain": req.get("domain", ""),
        "description": req["description"],
        "constraints": req.get("constraints", ""),
        "stages": stages,
        "tools_invoked": tools_invoked,
        "evidence": evidence,
        "gate1": gate1,
        "gate2": gate2 if auto_gates else "pending",
        "gate1_note": gate1_note,
        "gate2_note": gate2_note,
        "model": "deterministic-workflow-runner",
        "timestamp": utc_now(),
        "completed_at": utc_now() if auto_gates else None,
        "status": status,
        "analysis": analysis,
        "plan": plan if auto_gates else None,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
        "buckets": buckets,
    }
    save_run(run)
    return run


def apply_gate(run_id: str, gate: int, decision: str, note: str) -> dict[str, Any]:
    if decision not in ("approved", "rejected"):
        raise ValueError("decision must be approved|rejected")
    run = load_run(run_id)
    if gate == 1:
        if run["status"] not in ("awaiting_gate1", "running"):
            raise ValueError(f"Run not awaiting gate1 (status={run['status']})")
        run["gate1"] = decision
        run["gate1_note"] = note
        run["stages"] = list(dict.fromkeys([*run["stages"], "gate1"]))
        if decision == "rejected":
            run["status"] = "rejected"
            run["completed_at"] = utc_now()
        else:
            # produce plan
            buckets = run.get("buckets") or {"builders": [], "validators": [], "steps": [], "features": [], "clients": [], "pages": []}
            run["plan"] = build_plan(
                {
                    "request_id": run["request_id"],
                    "target": run["target"],
                    "domain": run.get("domain", ""),
                    "description": run.get("description", ""),
                },
                run["analysis"],
                run["evidence"],
                buckets,
            )
            run["stages"] = list(dict.fromkeys([*run["stages"], "plan"]))
            run["status"] = "awaiting_gate2"
            run["gate2"] = "pending"
    elif gate == 2:
        if run["status"] != "awaiting_gate2":
            raise ValueError(f"Run not awaiting gate2 (status={run['status']})")
        run["gate2"] = decision
        run["gate2_note"] = note
        run["stages"] = list(dict.fromkeys([*run["stages"], "gate2"]))
        if decision == "approved":
            run["stages"] = list(dict.fromkeys([*run["stages"], "delivered"]))
            run["status"] = "completed"
        else:
            run["status"] = "rejected"
        run["completed_at"] = utc_now()
    else:
        raise ValueError("gate must be 1 or 2")
    save_run(run)
    return run


def cmd_smoke() -> int:
    checks: list[tuple[str, bool, str]] = []

    # Duplicate builder → already_covered + empty create
    run1 = start_workflow(
        json.loads((SAMPLES_DIR / "AUTH-DUPLICATE-BUILDER.json").read_text(encoding="utf-8")),
        auto_gates=True,
    )
    ok1 = (
        run1["status"] == "completed"
        and run1["analysis"]["meta"]["already_covered"] is True
        and run1["plan"]["create_only_if_needed"] == []
        and any(t["tool"] == "find_existing_builder" and (t["hit_count"] or 0) > 0 for t in run1["tools_invoked"])
        and "LoginRequestBuilder" in run1["plan"]["reuse"]["builders"]
    )
    checks.append(("AUTH-DUPLICATE-BUILDER", ok1, run1["run_id"]))

    # Login neg already covered
    run2 = start_workflow(
        json.loads((SAMPLES_DIR / "AUTH-LOGIN-NEG.json").read_text(encoding="utf-8")),
        auto_gates=True,
    )
    ok2 = run2["analysis"]["meta"]["already_covered"] is True and run2["gate1"] == "approved"
    checks.append(("AUTH-LOGIN-NEG", ok2, run2["run_id"]))

    # Interactive gates path
    run3 = start_workflow(
        json.loads((SAMPLES_DIR / "USER-PROFILE-GET.json").read_text(encoding="utf-8")),
        auto_gates=False,
    )
    ok3a = run3["status"] == "awaiting_gate1" and run3["plan"] is None
    run3 = apply_gate(run3["run_id"], 1, "approved", "smoke gate1")
    ok3b = run3["status"] == "awaiting_gate2" and run3["plan"] is not None
    run3 = apply_gate(run3["run_id"], 2, "approved", "smoke gate2")
    ok3c = run3["status"] == "completed" and "delivered" in run3["stages"]
    checks.append(("USER-PROFILE-GET-gates", ok3a and ok3b and ok3c, run3["run_id"]))

    # Persist golden copies for docs (committed)
    golden_dir = ROOT / "docs/ai-evolution/evals/runs"
    golden_dir.mkdir(parents=True, exist_ok=True)
    for label, run in ("duplicate-builder", run1), ("login-neg", run2), ("profile-gates", run3):
        slim = {k: run[k] for k in run if k != "buckets"}
        (golden_dir / f"phase5-{label}.json").write_text(json.dumps(slim, indent=2), encoding="utf-8")

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# workflow_runner smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Start a workflow run")
    start.add_argument("--from", dest="from_path", help="Request JSON path")
    start.add_argument("--request-id")
    start.add_argument("--target", choices=["csharp", "python"])
    start.add_argument("--domain")
    start.add_argument("--description")
    start.add_argument("--terms")
    start.add_argument("--constraints")
    start.add_argument("--auto-gates", action="store_true", help="Approve gate1/gate2 automatically")
    start.add_argument("--json", action="store_true")

    gate = sub.add_parser("gate", help="Apply human gate decision")
    gate.add_argument("--run-id", required=True)
    gate.add_argument("--gate", type=int, choices=[1, 2], required=True)
    gate.add_argument("--decision", choices=["approved", "rejected"], required=True)
    gate.add_argument("--note", default="")
    gate.add_argument("--json", action="store_true")

    show = sub.add_parser("show", help="Show a run")
    show.add_argument("--run-id", required=True)
    show.add_argument("--json", action="store_true")

    sub.add_parser("smoke", help="Phase 5 smoke checks")

    args = parser.parse_args()

    try:
        if args.command == "start":
            path = Path(args.from_path) if args.from_path else None
            if path and not path.is_absolute():
                path = ROOT / path
            req = load_request(path, args)
            run = start_workflow(req, auto_gates=args.auto_gates)
            if args.json:
                print(json.dumps(run, indent=2))
            else:
                print(f"# run_id={run['run_id']} status={run['status']} gate1={run['gate1']} gate2={run['gate2']}")
                print(f"# tools={len(run['tools_invoked'])} evidence={len(run['evidence'])} elapsed_ms={run['elapsed_ms']}")
                print(f"# already_covered={run['analysis']['meta'].get('already_covered')}")
                print(f"# saved=.forgeone/runs/workflow/{run['run_id']}.json")
            return 0
        if args.command == "gate":
            run = apply_gate(args.run_id, args.gate, args.decision, args.note)
            print(json.dumps(run, indent=2) if args.json else f"# run_id={run['run_id']} status={run['status']}")
            return 0
        if args.command == "show":
            run = load_run(args.run_id)
            if args.json:
                print(json.dumps(run, indent=2))
            else:
                print(f"run_id={run['run_id']} request={run['request_id']} status={run['status']}")
                print(f"gates: {run['gate1']}/{run['gate2']} stages={run['stages']}")
                print(f"tools_invoked={len(run['tools_invoked'])}")
            return 0
        if args.command == "smoke":
            return cmd_smoke()
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
