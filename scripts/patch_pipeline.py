#!/usr/bin/env python3
"""Phase 7 controlled patch pipeline.

Flow: approved plan/recipe → validate paths → review_diff → (optional) apply + tests → Gate 3.
Never merges. Apply to the working tree only with --gate3-approved.

Usage:
  python3 scripts/patch_pipeline.py propose --recipe good-access-token-expired
  python3 scripts/patch_pipeline.py propose --recipe bad-sleep-support
  python3 scripts/patch_pipeline.py apply --proposal-id <id> --gate3-approved --run-tests
  python3 scripts/patch_pipeline.py smoke
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = ROOT / "tools/patches/v1/allowlist.json"
RECIPES_PATH = ROOT / "tools/patches/v1/recipes.json"
PROPOSALS_DIR = ROOT / ".forgeone/runs/patches"
sys.path.insert(0, str(ROOT / "scripts"))

from review_diff import review_text  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_allowlist() -> dict[str, Any]:
    return load_json(ALLOWLIST_PATH)


def load_recipes() -> dict[str, dict[str, Any]]:
    data = load_json(RECIPES_PATH)
    return {r["id"]: r for r in data["recipes"]}


def paths_from_diff(diff_text: str) -> list[str]:
    paths: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            paths.append(line[6:].strip())
    return list(dict.fromkeys(paths))


def validate_paths(paths: list[str], allowlist: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    prefixes = allowlist["allowed_path_prefixes"]
    denied = allowlist.get("denied_path_globs", [])
    max_files = int(allowlist.get("max_files_touched", 5))

    if len(paths) == 0:
        errors.append("diff touches no files")
    if len(paths) > max_files:
        errors.append(f"touches {len(paths)} files; max is {max_files}")

    for path in paths:
        if not any(path.startswith(p) for p in prefixes):
            errors.append(f"path not allowlisted: {path}")
        for glob in denied:
            if fnmatch.fnmatch(path, glob):
                errors.append(f"path denied by glob {glob}: {path}")
    return errors


def load_workflow_run(run_id: str) -> dict[str, Any]:
    path = ROOT / ".forgeone/runs/workflow" / f"{run_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"workflow run not found: {run_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_proposal(proposal: dict[str, Any]) -> Path:
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    path = PROPOSALS_DIR / f"{proposal['proposal_id']}.json"
    diff_path = PROPOSALS_DIR / f"{proposal['proposal_id']}.diff"
    diff_path.write_text(proposal["diff_text"], encoding="utf-8")
    proposal["diff_path"] = str(diff_path.relative_to(ROOT))
    # avoid duplicating huge diff twice in JSON optionally keep it
    path.write_text(json.dumps({k: v for k, v in proposal.items() if k != "diff_text"}, indent=2), encoding="utf-8")
    # also store diff_text in sidecar only; reload needs it
    meta = json.loads(path.read_text(encoding="utf-8"))
    meta["diff_text"] = proposal["diff_text"]
    path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return path


def load_proposal(proposal_id: str) -> dict[str, Any]:
    path = PROPOSALS_DIR / f"{proposal_id}.json"
    if not path.is_file():
        raise FileNotFoundError(proposal_id)
    return json.loads(path.read_text(encoding="utf-8"))


def propose(
    recipe_id: str | None,
    run_id: str | None,
    gate2_note: str,
) -> dict[str, Any]:
    allowlist = load_allowlist()
    recipes = load_recipes()

    plan_meta: dict[str, Any] = {
        "gate2": "approved",
        "gate2_note": gate2_note,
        "source": "recipe",
    }

    if run_id:
        run = load_workflow_run(run_id)
        if run.get("gate2") != "approved":
            raise ValueError(f"workflow run {run_id} gate2={run.get('gate2')}; require approved")
        plan_meta = {
            "gate2": "approved",
            "gate2_note": run.get("gate2_note", ""),
            "source": "workflow_run",
            "run_id": run_id,
            "request_id": run.get("request_id"),
            "plan_already_covered": run.get("plan", {}).get("meta", {}).get("already_covered"),
        }
        if plan_meta["plan_already_covered"]:
            raise ValueError("refusing to patch: plan marked already_covered")
        if not recipe_id:
            raise ValueError("when using --from-run, also pass --recipe for v1 deterministic patch body")

    if not recipe_id:
        raise ValueError("recipe is required in v1")
    if recipe_id not in recipes:
        raise KeyError(f"unknown recipe {recipe_id}")

    recipe = recipes[recipe_id]
    diff_rel = recipe["diff"]
    diff_text = (ROOT / diff_rel).read_text(encoding="utf-8")
    paths = paths_from_diff(diff_text)
    path_errors = validate_paths(paths, allowlist)

    findings = review_text(diff_text, diff_rel)
    codes = sorted({f["code"] for f in findings})
    block_severities = set(allowlist.get("block_severities", ["high"]))
    blocking = [f for f in findings if f.get("severity") in block_severities]
    review_clean = len(blocking) == 0

    status = "blocked" if path_errors or not review_clean else "awaiting_gate3"

    proposal = {
        "contract": "patch-proposal.v1",
        "proposal_id": new_id(),
        "timestamp": utc_now(),
        "recipe_id": recipe_id,
        "request_id": recipe.get("request_id"),
        "description": recipe.get("description"),
        "plan_meta": plan_meta,
        "paths": paths,
        "path_errors": path_errors,
        "review": {
            "clean": review_clean,
            "finding_count": len(findings),
            "blocking_count": len(blocking),
            "codes": codes,
            "findings": findings,
        },
        "gate3": "pending" if status == "awaiting_gate3" else "rejected",
        "gate3_note": "",
        "status": status,
        "applied": False,
        "tests": None,
        "diff_text": diff_text,
        "diff_recipe": diff_rel,
    }
    save_proposal(proposal)
    return proposal


def run_dotnet_test() -> dict[str, Any]:
    proc = subprocess.run(
        ["dotnet", "test", "--verbosity", "minimal"],
        cwd=ROOT / "labs/csharp-reqnroll-lab",
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": "dotnet test",
        "exit_code": proc.returncode,
        "passed": proc.returncode == 0,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-1000:],
    }


def apply_proposal(proposal_id: str, gate3_approved: bool, run_tests: bool, restore_after: bool) -> dict[str, Any]:
    if not gate3_approved:
        raise ValueError("refusing apply without --gate3-approved")

    proposal = load_proposal(proposal_id)
    if proposal["status"] == "blocked":
        raise ValueError("proposal is blocked (path errors or high-severity review findings)")
    if proposal["gate3"] == "rejected":
        raise ValueError("proposal gate3 rejected")

    allowlist = load_allowlist()
    path_errors = validate_paths(proposal["paths"], allowlist)
    if path_errors:
        raise ValueError(f"path validation failed: {path_errors}")

    findings = review_text(proposal["diff_text"], proposal.get("diff_path", "proposal.diff"))
    blocking = [f for f in findings if f.get("severity") in set(allowlist.get("block_severities", ["high"]))]
    if blocking:
        proposal["status"] = "blocked"
        proposal["gate3"] = "rejected"
        proposal["gate3_note"] = "blocked on re-review before apply"
        proposal["review"]["findings"] = findings
        save_proposal(proposal)
        raise ValueError("re-review found blocking findings; apply aborted")

    # Snapshot for restore (works even if files are not yet git-tracked)
    snapshots: dict[str, str | None] = {}
    if restore_after:
        for rel in proposal["paths"]:
            path = ROOT / rel
            snapshots[rel] = path.read_text(encoding="utf-8") if path.is_file() else None

    diff_file = PROPOSALS_DIR / f"{proposal_id}.diff"
    diff_file.write_text(proposal["diff_text"], encoding="utf-8")

    check = subprocess.run(
        ["git", "apply", "--check", str(diff_file)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if check.returncode != 0:
        raise RuntimeError(f"git apply --check failed: {check.stderr}")

    applied = subprocess.run(
        ["git", "apply", str(diff_file)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if applied.returncode != 0:
        raise RuntimeError(f"git apply failed: {applied.stderr}")

    proposal["applied"] = True
    proposal["gate3"] = "approved"
    proposal["gate3_note"] = "approved via --gate3-approved"
    proposal["status"] = "applied"
    proposal["applied_at"] = utc_now()

    if run_tests:
        proposal["tests"] = run_dotnet_test()
        if not proposal["tests"]["passed"]:
            proposal["status"] = "tests_failed"

    if restore_after:
        for rel, content in snapshots.items():
            path = ROOT / rel
            if content is None:
                if path.exists():
                    path.unlink()
            else:
                path.write_text(content, encoding="utf-8")
        proposal["restored_after_smoke"] = True
        if proposal["status"] == "applied":
            proposal["status"] = "applied_restored"

    save_proposal(proposal)
    return proposal


def cmd_smoke() -> int:
    checks: list[tuple[str, bool, str]] = []

    bad = propose("bad-sleep-support", None, "smoke")
    ok_bad = bad["status"] == "blocked" and "STAB-SLEEP-CS" in bad["review"]["codes"]
    checks.append(("bad_recipe_blocked", ok_bad, str(bad["review"]["codes"])))

    good = propose("good-access-token-expired", None, "smoke")
    ok_good = good["status"] == "awaiting_gate3" and good["review"]["clean"] is True
    checks.append(("good_recipe_awaiting_gate3", ok_good, good["status"]))

    # Apply + test + restore
    try:
        applied = apply_proposal(good["proposal_id"], gate3_approved=True, run_tests=True, restore_after=True)
        ok_apply = applied.get("tests", {}).get("passed") is True and applied.get("restored_after_smoke") is True
        detail = f"tests={applied.get('tests', {}).get('passed')} status={applied.get('status')}"
    except Exception as exc:  # noqa: BLE001 — smoke must report
        ok_apply = False
        detail = str(exc)
    checks.append(("good_apply_tests_restore", ok_apply, detail))

    # Refuse apply without gate3
    try:
        apply_proposal(good["proposal_id"], gate3_approved=False, run_tests=False, restore_after=False)
        ok_refuse = False
        detail_r = "should have refused"
    except ValueError as exc:
        ok_refuse = "gate3-approved" in str(exc)
        detail_r = str(exc)
    checks.append(("refuse_without_gate3", ok_refuse, detail_r))

    # Persist golden summary
    out = ROOT / "docs/ai-evolution/evals/patch-pipeline-baseline.json"
    out.write_text(
        json.dumps(
            {
                "bad_proposal_id": bad["proposal_id"],
                "good_proposal_id": good["proposal_id"],
                "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# patch_pipeline smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prop = sub.add_parser("propose", help="Create a patch proposal from recipe (+ optional workflow run)")
    prop.add_argument("--recipe", required=True)
    prop.add_argument("--from-run", dest="run_id", help="Workflow run id with gate2=approved")
    prop.add_argument("--gate2-note", default="manual/recipe")
    prop.add_argument("--json", action="store_true")

    app = sub.add_parser("apply", help="Apply proposal after Gate 3 approval")
    app.add_argument("--proposal-id", required=True)
    app.add_argument("--gate3-approved", action="store_true")
    app.add_argument("--run-tests", action="store_true")
    app.add_argument("--restore-after", action="store_true", help="git checkout touched files after tests (smoke)")
    app.add_argument("--json", action="store_true")

    show = sub.add_parser("show", help="Show proposal")
    show.add_argument("--proposal-id", required=True)
    show.add_argument("--json", action="store_true")

    sub.add_parser("smoke", help="Phase 7 smoke")

    args = parser.parse_args()
    try:
        if args.command == "propose":
            proposal = propose(args.recipe, args.run_id, args.gate2_note)
            if args.json:
                print(json.dumps(proposal, indent=2))
            else:
                print(
                    f"# proposal_id={proposal['proposal_id']} status={proposal['status']} "
                    f"review_clean={proposal['review']['clean']} codes={proposal['review']['codes']}"
                )
                print(f"# saved=.forgeone/runs/patches/{proposal['proposal_id']}.json")
            return 0 if proposal["status"] != "failed" else 1
        if args.command == "apply":
            proposal = apply_proposal(
                args.proposal_id,
                gate3_approved=args.gate3_approved,
                run_tests=args.run_tests,
                restore_after=args.restore_after,
            )
            print(json.dumps(proposal, indent=2) if args.json else f"# status={proposal['status']} applied={proposal['applied']}")
            return 0 if proposal["status"] in ("applied", "applied_restored") else 1
        if args.command == "show":
            proposal = load_proposal(args.proposal_id)
            print(json.dumps(proposal, indent=2) if args.json else f"# {proposal['proposal_id']} {proposal['status']}")
            return 0
        if args.command == "smoke":
            return cmd_smoke()
    except (ValueError, FileNotFoundError, KeyError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
