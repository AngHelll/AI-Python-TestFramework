#!/usr/bin/env python3
"""Smoke for lab MCP bridge (+ optional MCP SDK protocol check).

Always validates LabMcpBridge ↔ registry ↔ tools_runner.
If `mcp` is installed, also checks FastMCP tool registration.

Usage:
  python3 scripts/mcp_lab_smoke.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lab_mcp_bridge import BLOCKED_TOOL_NAMES, LabMcpBridge  # noqa: E402
from tools_runner import load_registry  # noqa: E402

BASELINE = ROOT / "docs/ai-evolution/evals/mcp-lab-baseline.json"


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    bridge = LabMcpBridge(no_audit=True)
    registry = load_registry()
    reg_names = sorted(t["name"] for t in registry["tools"])
    bridge_names = sorted(bridge.tool_names())

    ok_list = bridge_names == reg_names and len(reg_names) >= 1
    checks.append(("bridge_lists_registry", ok_list, f"count={len(reg_names)}"))

    result = bridge.invoke(
        "find_existing_builder",
        {"target": "csharp", "terms": "LoginRequestBuilder", "limit": "5"},
    )
    payload = json.dumps(result.get("result", {}))
    ok_find = result.get("ok") is True and "LoginRequestBuilder" in payload
    checks.append(("bridge_find_builder", ok_find, result.get("invocation_id", "")))

    review = bridge.invoke("review_diff", {"fixture": "uc05"})
    codes = (review.get("result") or {}).get("codes") or []
    ok_review = review.get("ok") is True and "DUP-BUILDER" in codes
    checks.append(("bridge_review_uc05", ok_review, str(codes)))

    blocked = False
    try:
        bridge.invoke("apply_patch", {})
    except PermissionError:
        blocked = True
    checks.append(("bridge_blocks_apply", blocked, "apply_patch"))

    unknown = False
    try:
        bridge.invoke("not_a_real_tool", {})
    except Exception:
        unknown = True
    checks.append(("bridge_rejects_unknown", unknown, "not_a_real_tool"))

    # Optional SDK surface
    mcp_status = "SKIP"
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401

        import mcp_lab_server as server_mod

        tool_fns = ["list_lab_tools", "invoke_lab_tool", "choose_gate2_recipe"]
        ok_fns = all(hasattr(server_mod, name) for name in tool_fns)
        listed = server_mod.list_lab_tools()
        invoked = server_mod.invoke_lab_tool(
            "find_existing_builder",
            json.dumps({"target": "csharp", "terms": "LoginRequestBuilder", "limit": 5}),
        )
        chosen = server_mod.choose_gate2_recipe(
            "AUTH-DUPLICATE-BUILDER",
            "LoginRequestBuilder",
            propose=False,
        )
        chosen_obj = json.loads(chosen)
        ok_sdk = (
            ok_fns
            and "find_existing_builder" in listed
            and "LoginRequestBuilder" in invoked
            and chosen_obj.get("action") == "skip"
        )
        mcp_status = "PASS" if ok_sdk else "FAIL"
        checks.append(("mcp_sdk_tools", ok_sdk, mcp_status))
        checks.append(("mcp_choose_gate2_recipe", chosen_obj.get("action") == "skip", chosen_obj.get("action", "")))
    except ImportError:
        checks.append(("mcp_sdk_tools", True, "SKIP (use .venv-mcp + requirements-mcp.txt)"))
        checks.append(("mcp_choose_gate2_recipe", True, "SKIP (no SDK)"))
        mcp_status = "SKIP"

    baseline = {
        "contract": "mcp-lab-bridge.v1",
        "registry_version": registry.get("version"),
        "tool_count": len(reg_names),
        "blocked_names": sorted(BLOCKED_TOOL_NAMES),
        "mcp_sdk": mcp_status,
        "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(baseline, indent=2), encoding="utf-8")

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# mcp_lab smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    print(f"# baseline={BASELINE.relative_to(ROOT)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
