#!/usr/bin/env python3
"""MCP stdio server for AI-Python-TestFramework lab tools.

Wraps tools_runner via LabMcpBridge. Does **not** reimplement search or apply patches.

Requires: pip install -r requirements-mcp.txt

Usage (Cursor / Claude Desktop mcp.json):
  {
    "mcpServers": {
      "ai-python-lab": {
        "command": "python3",
        "args": ["/absolute/path/to/AI-Python-TestFramework/scripts/mcp_lab_server.py"]
      }
    }
  }

Run:
  python3 scripts/mcp_lab_server.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lab_mcp_bridge import LabMcpBridge  # noqa: E402
from gate2_recipe_chat import (  # noqa: E402
    build_plan_for_request,
    deterministic_choose,
    load_recipes,
    maybe_propose,
)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover — smoke handles missing SDK
    print(
        "ERROR: mcp package not installed. Run: pip install -r requirements-mcp.txt",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


bridge = LabMcpBridge(no_audit=False)
mcp = FastMCP(
    "ai-python-testframework-lab",
    instructions=(
        "Allowlisted lab automation tools via tools_runner. "
        "Reuse Before Create. Never apply patches through MCP — "
        "human Gate 3 uses patch_pipeline.py apply --gate3-approved. "
        "After Gate 2, use choose_gate2_recipe to pick an allowlisted recipe (propose optional)."
    ),
)


@mcp.tool()
def list_lab_tools() -> str:
    """List allowlisted tools from the lab registry (tools/registry/v1)."""
    return bridge.list_tools_json()


@mcp.tool()
def invoke_lab_tool(tool: str, args_json: str = "{}") -> str:
    """Invoke one allowlisted lab tool by name.

    Args:
        tool: Registry tool name (e.g. find_existing_builder, review_diff, propose_patch).
        args_json: JSON object of parameters (values coerced to strings for tools_runner).

    Examples:
        tool=find_existing_builder args_json={"target":"csharp","terms":"LoginRequestBuilder","limit":5}
        tool=review_diff args_json={"fixture":"uc05"}
        tool=propose_patch args_json={"recipe":"good-access-token-expired"}
    """
    return bridge.invoke_json(tool, args_json)


@mcp.tool()
def choose_gate2_recipe(
    request_id: str,
    terms: str,
    propose: bool = False,
    target: str = "csharp",
) -> str:
    """After Gate 2: choose an allowlisted patch recipe (or skip if already_covered).

    Deterministic chooser — no LLM required. Never applies patches.
    Set propose=true to create a proposal awaiting Gate 3.

    Args:
        request_id: e.g. AUTH-TOKEN-REFRESH or AUTH-DUPLICATE-BUILDER
        terms: search/intent terms used for plan context
        propose: if true, run propose_patch for the chosen recipe
        target: csharp | python
    """
    import json

    recipes = load_recipes()
    plan = build_plan_for_request(request_id, terms, target=target)
    choice = deterministic_choose(request_id, terms, plan, recipes)
    choice["plan_already_covered"] = bool(plan.get("meta", {}).get("already_covered"))
    result = maybe_propose(choice, propose)
    return json.dumps(result, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
