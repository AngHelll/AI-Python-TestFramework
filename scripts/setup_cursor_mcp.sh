#!/usr/bin/env bash
# Ensure .venv-mcp exists and print Cursor MCP status for this lab.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -x .venv-mcp/bin/python ]]; then
  echo "==> creating .venv-mcp"
  python3 -m venv .venv-mcp
  .venv-mcp/bin/pip install -r requirements-mcp.txt
fi

echo "==> mcp_lab smoke (with SDK)"
.venv-mcp/bin/python scripts/mcp_lab_smoke.py

MCP_JSON="$ROOT/.cursor/mcp.json"
if [[ -f "$MCP_JSON" ]]; then
  echo "==> Cursor project MCP config present: .cursor/mcp.json"
  echo "    Server: ai-python-lab → scripts/mcp_lab_server.py"
  echo "    Reload: Cursor Settings → MCP → refresh, or restart Cursor"
else
  echo "ERROR: missing $MCP_JSON"
  exit 1
fi

echo "==> done"
