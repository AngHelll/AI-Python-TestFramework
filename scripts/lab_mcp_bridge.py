#!/usr/bin/env python3
"""Lab MCP bridge — thin façade over tools_runner (no allowlist bypass).

This module has **no** dependency on the `mcp` package. The MCP stdio server
(`mcp_lab_server.py`) imports it when the SDK is installed.

Contract: never expose apply/merge/push. Only registry tools via tools_runner.invoke.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tools_runner import invoke as tools_invoke  # noqa: E402
from tools_runner import load_registry  # noqa: E402

BLOCKED_TOOL_NAMES = frozenset(
    {
        "apply_patch",
        "apply",
        "git_push",
        "git_commit",
        "arbitrary_shell",
        "write_files",
    }
)


class LabMcpBridge:
    """Allowlisted tool façade for MCP / other hosts."""

    def __init__(self, no_audit: bool = False) -> None:
        self.no_audit = no_audit
        self.registry = load_registry()

    def list_tools(self) -> list[dict[str, Any]]:
        tools = []
        for tool in self.registry["tools"]:
            tools.append(
                {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "permissions": tool.get("permissions", []),
                    "params": tool.get("params", {}),
                }
            )
        return tools

    def tool_names(self) -> list[str]:
        return [t["name"] for t in self.list_tools()]

    def invoke(self, tool: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        name = (tool or "").strip()
        if not name:
            raise ValueError("tool name required")
        if name in BLOCKED_TOOL_NAMES:
            raise PermissionError(
                f"Tool {name!r} is blocked at MCP bridge (no apply/merge/shell). "
                "Use patch_pipeline.py apply --gate3-approved only with human Gate 3."
            )
        # Ensure tool exists in registry (tools_invoke also checks)
        _ = next(t for t in self.registry["tools"] if t["name"] == name)

        raw_args = {k: str(v) for k, v in (args or {}).items() if v is not None}
        record = tools_invoke(name, raw_args, no_audit=self.no_audit)
        return {
            "ok": bool(record.get("ok")),
            "tool": name,
            "invocation_id": record.get("invocation_id"),
            "params": record.get("params"),
            "result": record.get("result"),
            "note": "Apply patches only via scripts/patch_pipeline.py apply --gate3-approved",
        }

    def invoke_json(self, tool: str, args_json: str = "{}") -> str:
        try:
            args = json.loads(args_json) if args_json.strip() else {}
        except json.JSONDecodeError as exc:
            raise ValueError(f"args_json must be a JSON object: {exc}") from exc
        if not isinstance(args, dict):
            raise ValueError("args_json must decode to an object")
        return json.dumps(self.invoke(tool, args), indent=2)

    def list_tools_json(self) -> str:
        return json.dumps(
            {
                "registry_version": self.registry.get("version"),
                "mode": self.registry.get("mode"),
                "denied": self.registry.get("denied", []),
                "tools": self.list_tools(),
                "mcp_note": "Wrapper over tools_runner — allowlists unchanged",
            },
            indent=2,
        )
