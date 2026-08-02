#!/usr/bin/env bash
# Portable launcher for Cursor MCP (resolves repo root from this script).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/.venv-mcp/bin/python"
SERVER="$ROOT/scripts/mcp_lab_server.py"

if [[ ! -x "$PY" ]]; then
  echo "ERROR: missing $PY — run: bash scripts/setup_cursor_mcp.sh" >&2
  exit 1
fi

export PYTHONUNBUFFERED=1
exec "$PY" "$SERVER"
