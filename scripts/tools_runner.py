#!/usr/bin/env python3
"""Phase 4 read-only tools runner.

Agents must invoke tools ONLY through this entrypoint (not arbitrary shell).

Usage:
  python3 scripts/tools_runner.py list
  python3 scripts/tools_runner.py invoke find_existing_builder --arg target=csharp --arg terms=LoginRequestBuilder
  python3 scripts/tools_runner.py invoke detect_forbidden_patterns --arg target=csharp
  python3 scripts/tools_runner.py smoke
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "tools/registry/v1/registry.json"
sys.path.insert(0, str(ROOT / "scripts"))

from find_existing_components import SEARCH_ROOTS, iter_files, resolve_terms, scan  # noqa: E402
from review_diff import review_fixture, review_path  # noqa: E402
from patch_pipeline import propose as propose_patch_recipe  # noqa: E402

TERM_PATTERN = re.compile(r"^[A-Za-z0-9_,\-.\s]{1,120}$")

FORBIDDEN_PATTERNS = [
    ("AP-03-sleep-csharp", re.compile(r"Thread\.Sleep\s*\("), "Thread.Sleep"),
    ("AP-03-sleep-python", re.compile(r"\btime\.sleep\s*\("), "time.sleep"),
    ("AP-05-password-literal", re.compile(r"""password\s*=\s*['\"](?!valid_password|wrong_password)[^'\"]+['\"]""", re.I), "hard-coded password-like literal"),
    ("AP-05-api-key", re.compile(r"""(api[_-]?key|secret)\s*=\s*['\"][^'\"]+['\"]""", re.I), "hard-coded secret-like literal"),
]

NAMING_RULES = {
    "builder": re.compile(r"^[A-Z][A-Za-z0-9]*Builder$"),
    "validator": re.compile(r"^[A-Z][A-Za-z0-9]*Validator$"),
    "steps": re.compile(r"^[A-Z][A-Za-z0-9]*Steps$"),
    "feature": re.compile(r"^[A-Z][A-Za-z0-9]*(\.feature)?$"),
}


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def tool_by_name(registry: dict[str, Any], name: str) -> dict[str, Any]:
    for tool in registry["tools"]:
        if tool["name"] == name:
            return tool
    raise KeyError(f"Unknown tool: {name}. Use: tools_runner.py list")


def parse_args_list(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid --arg {pair!r}; expected key=value")
        key, value = pair.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def validate_params(tool: dict[str, Any], raw: dict[str, str]) -> dict[str, Any]:
    schema = tool.get("params", {})
    validated: dict[str, Any] = {}

    for name, spec in schema.items():
        required = bool(spec.get("required"))
        if name not in raw:
            if required and "default" not in spec:
                raise ValueError(f"Missing required param: {name}")
            if "default" in spec:
                validated[name] = spec["default"]
            continue

        value: Any = raw[name]
        ptype = spec.get("type")
        if ptype == "enum":
            if value not in spec["values"]:
                raise ValueError(f"Param {name}={value!r} not in {spec['values']}")
        elif ptype == "int":
            value = int(value)
            if value < spec.get("min", value) or value > spec.get("max", value):
                raise ValueError(f"Param {name}={value} out of range")
        elif ptype == "string":
            max_length = spec.get("max_length", 120)
            if len(value) > max_length:
                raise ValueError(f"Param {name} exceeds max_length {max_length}")
            if name == "terms" and not TERM_PATTERN.match(value):
                raise ValueError("Param terms has invalid characters")
        validated[name] = value

    unknown = set(raw) - set(schema)
    if unknown:
        raise ValueError(f"Unknown params: {sorted(unknown)}")
    return validated


def audit_write(registry: dict[str, Any], record: dict[str, Any]) -> Path:
    audit_dir = ROOT / registry["audit_dir"]
    audit_dir.mkdir(parents=True, exist_ok=True)
    path = audit_dir / f"{record['invocation_id']}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return path


def handle_find_components(tool: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    target = params["target"]
    terms = resolve_terms(None, params["terms"])
    limit = int(params.get("limit", 5))
    kinds = tool.get("kinds")
    hits = scan(target, terms, limit=limit, kinds=kinds)
    return {"hits": hits, "count": len(hits), "terms": terms, "kinds": kinds}


def handle_detect_forbidden(params: dict[str, Any]) -> dict[str, Any]:
    target = params["target"]
    limit = int(params.get("limit", 50))
    roots = SEARCH_ROOTS[target]
    findings: list[dict[str, str]] = []

    for kind, directory in roots.items():
        for path in iter_files(directory):
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = path.relative_to(ROOT).as_posix()
            for code, pattern, label in FORBIDDEN_PATTERNS:
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(
                        {
                            "code": code,
                            "label": label,
                            "path": rel,
                            "kind": kind,
                            "line": str(line),
                            "snippet": match.group(0)[:80],
                        }
                    )
                    if len(findings) >= limit:
                        return {"findings": findings, "count": len(findings), "truncated": True}
    return {"findings": findings, "count": len(findings), "truncated": False}


def handle_validate_naming(params: dict[str, Any]) -> dict[str, Any]:
    kind = params["kind"]
    name = params["name"]
    pattern = NAMING_RULES[kind]
    check_name = name[: -len(".feature")] if kind == "feature" and name.endswith(".feature") else name
    if kind == "feature":
        ok = bool(re.match(r"^[A-Z][A-Za-z0-9]*$", check_name))
    else:
        ok = bool(pattern.match(check_name))
    return {
        "kind": kind,
        "name": name,
        "valid": ok,
        "rule": pattern.pattern,
        "hint": {
            "builder": "Use PascalCase ending with Builder (e.g. LoginRequestBuilder)",
            "validator": "Use PascalCase ending with Validator",
            "steps": "Use PascalCase ending with Steps",
            "feature": "Use PascalCase feature stem (e.g. TokenRefresh)",
        }[kind],
    }


def handle_get_changed_files(params: dict[str, Any]) -> dict[str, Any]:
    prefix = params.get("prefix", "labs/csharp-reqnroll-lab")
    # Fixed argv — no user-controlled shell string.
    proc = subprocess.run(
        ["git", "status", "--porcelain", "-u"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return {"error": "git_status_failed", "stderr": proc.stderr.strip(), "files": []}

    files: list[dict[str, str]] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        status, path = line[:2].strip(), line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.startswith(prefix):
            files.append({"status": status, "path": path})
    return {"prefix": prefix, "files": files, "count": len(files)}


def handle_review_diff(params: dict[str, Any]) -> dict[str, Any]:
    fixture = params.get("fixture")
    path = params.get("path")
    category = params.get("category")
    if fixture:
        return review_fixture(str(fixture), category=str(category) if category else None)
    if path:
        rel = str(path)
        if not (
            rel.startswith("knowledge/examples/review/")
            or rel.startswith("labs/csharp-reqnroll-lab/")
            or rel.startswith("features/")
            or rel.startswith("pages/")
        ):
            raise ValueError("review_diff path not allowlisted")
        result = review_path(rel)
        if category:
            result["findings"] = [f for f in result["findings"] if f.get("category") == category]
            result["codes"] = sorted({f["code"] for f in result["findings"]})
            result["finding_count"] = len(result["findings"])
        return result
    raise ValueError("review_diff requires fixture or path")


def handle_propose_patch(params: dict[str, Any]) -> dict[str, Any]:
    proposal = propose_patch_recipe(str(params["recipe"]), None, "tools_runner.propose_patch")
    # Do not return full diff_text to keep tool payload smaller; path is enough
    return {
        "proposal_id": proposal["proposal_id"],
        "status": proposal["status"],
        "request_id": proposal.get("request_id"),
        "paths": proposal["paths"],
        "path_errors": proposal["path_errors"],
        "review": {
            "clean": proposal["review"]["clean"],
            "codes": proposal["review"]["codes"],
            "blocking_count": proposal["review"]["blocking_count"],
            "finding_count": proposal["review"]["finding_count"],
        },
        "gate3": proposal["gate3"],
        "diff_path": proposal.get("diff_path"),
        "note": "Apply only via: python3 scripts/patch_pipeline.py apply --proposal-id … --gate3-approved",
    }


def invoke(tool_name: str, raw_args: dict[str, str], no_audit: bool = False) -> dict[str, Any]:
    registry = load_registry()
    if registry.get("mode") != "read_only":
        raise RuntimeError("Registry mode must be read_only")

    tool = tool_by_name(registry, tool_name)
    params = validate_params(tool, raw_args)
    invocation_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    started = datetime.now(timezone.utc).isoformat()

    handler = tool["handler"]
    if handler == "find_components":
        result = handle_find_components(tool, params)
    elif handler == "detect_forbidden":
        result = handle_detect_forbidden(params)
    elif handler == "validate_naming":
        result = handle_validate_naming(params)
    elif handler == "get_changed_files":
        result = handle_get_changed_files(params)
    elif handler == "review_diff":
        result = handle_review_diff(params)
    elif handler == "propose_patch":
        result = handle_propose_patch(params)
    else:
        raise RuntimeError(f"Unsupported handler: {handler}")

    record = {
        "invocation_id": invocation_id,
        "timestamp": started,
        "tool": tool_name,
        "permissions": tool.get("permissions", []),
        "params": params,
        "ok": True,
        "result_summary": {
            "keys": sorted(result.keys()),
            "count": result.get("count", result.get("finding_count", result.get("valid"))),
        },
        "result": result,
    }
    if not no_audit:
        audit_path = audit_write(registry, record)
        record["audit_path"] = str(audit_path.relative_to(ROOT))
    return record


def cmd_list() -> int:
    registry = load_registry()
    print(f"# tools registry v{registry['version']} mode={registry['mode']}")
    print(f"# denied: {', '.join(registry.get('denied', []))}")
    for tool in registry["tools"]:
        print(f"- {tool['name']}: {tool['description']}")
        params = ", ".join(
            f"{n}{'*' if p.get('required') else ''}" for n, p in tool.get("params", {}).items()
        )
        print(f"  params: {params}")
    return 0


def cmd_invoke(tool_name: str, arg_pairs: list[str], as_json: bool, no_audit: bool) -> int:
    try:
        raw = parse_args_list(arg_pairs)
        record = invoke(tool_name, raw, no_audit=no_audit)
    except (KeyError, ValueError, RuntimeError) as exc:
        err = {"ok": False, "error": str(exc), "tool": tool_name}
        print(json.dumps(err, indent=2) if as_json else f"ERROR: {exc}")
        return 2

    if as_json:
        print(json.dumps(record, indent=2))
    else:
        print(f"# invoke {tool_name} id={record['invocation_id']}")
        if "audit_path" in record:
            print(f"# audit: {record['audit_path']}")
        print(json.dumps(record["result"], indent=2))
    return 0


def cmd_smoke() -> int:
    """Deterministic smoke checks for Phase 4 exit criteria."""
    checks: list[tuple[str, bool, str]] = []

    # 1) find builder
    r1 = invoke(
        "find_existing_builder",
        {"target": "csharp", "terms": "LoginRequestBuilder", "limit": "5"},
        no_audit=True,
    )
    paths = [h["path"] for h in r1["result"]["hits"]]
    ok1 = any(p.endswith("LoginRequestBuilder.cs") for p in paths)
    checks.append(("find_existing_builder", ok1, str(paths[:3])))

    # 2) validate naming reject duplicate-style
    r2 = invoke(
        "validate_naming",
        {"kind": "builder", "name": "LoginRequestBuilder2"},
        no_audit=True,
    )
    # LoginRequestBuilder2 matches *Builder regex — still valid shape; check good name
    r2b = invoke(
        "validate_naming",
        {"kind": "builder", "name": "loginRequest"},
        no_audit=True,
    )
    ok2 = r2b["result"]["valid"] is False
    checks.append(("validate_naming_rejects_bad", ok2, json.dumps(r2b["result"])))

    # 3) unknown tool rejected
    try:
        invoke("rm_rf_root", {}, no_audit=True)
        ok3 = False
        detail3 = "should have raised"
    except KeyError as exc:
        ok3 = True
        detail3 = str(exc)
    checks.append(("unknown_tool_rejected", ok3, detail3))

    # 4) forbidden target rejected
    try:
        invoke(
            "find_existing_builder",
            {"target": "knowledge", "terms": "x"},
            no_audit=True,
        )
        ok4 = False
        detail4 = "should reject knowledge target for builder tool"
    except ValueError as exc:
        ok4 = True
        detail4 = str(exc)
    checks.append(("target_allowlist", ok4, detail4))

    # 5) detect_forbidden runs
    r5 = invoke("detect_forbidden_patterns", {"target": "csharp", "limit": "20"}, no_audit=True)
    ok5 = "findings" in r5["result"]
    checks.append(("detect_forbidden_patterns", ok5, f"count={r5['result'].get('count')}"))

    # 6) find_knowledge
    r6 = invoke(
        "find_knowledge",
        {"target": "knowledge", "terms": "component-catalog", "limit": "5"},
        no_audit=True,
    )
    ok6 = any("component-catalog.md" in h["path"] for h in r6["result"]["hits"])
    checks.append(("find_knowledge", ok6, str([h["path"] for h in r6["result"]["hits"][:3]])))

    # 7) review_diff UC-05
    r7 = invoke("review_diff", {"fixture": "uc05"}, no_audit=True)
    ok7 = r7["result"].get("pass") is True and "DUP-BUILDER" in r7["result"].get("codes", [])
    checks.append(("review_diff_uc05", ok7, str(r7["result"].get("codes"))))

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# tools_runner smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List registered tools")

    inv = sub.add_parser("invoke", help="Invoke a registered tool")
    inv.add_argument("tool")
    inv.add_argument("--arg", action="append", default=[], help="key=value (repeatable)")
    inv.add_argument("--json", action="store_true")
    inv.add_argument("--no-audit", action="store_true", help="Skip writing audit file")

    sub.add_parser("smoke", help="Run Phase 4 smoke checks")

    args = parser.parse_args()
    if args.command == "list":
        return cmd_list()
    if args.command == "invoke":
        return cmd_invoke(args.tool, args.arg, args.json, args.no_audit)
    if args.command == "smoke":
        return cmd_smoke()
    return 2


if __name__ == "__main__":
    sys.exit(main())
