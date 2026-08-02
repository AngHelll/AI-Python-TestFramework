# Eval 014 — MCP lab wrapper

**Fecha:** 2026-07-31  
**Command:** `python3 scripts/mcp_lab_smoke.py` (SDK: `.venv-mcp/bin/python …`)  
**Doc:** [tools/mcp/v1/README.md](../../../tools/mcp/v1/README.md)  
**Baseline:** [mcp-lab-baseline.json](mcp-lab-baseline.json)  
**ADR:** [ADR-002](../../../knowledge/decisions/ADR-002-orchestration.md)

## Objetivo

Segundo cliente de las mismas tools allowlisteadas vía MCP stdio, sin bypass de registry ni apply silencioso.

## Criterios

| Check | Esperado |
|-------|----------|
| bridge_lists_registry | nombres = registry |
| bridge_find_builder | LoginRequestBuilder |
| bridge_review_uc05 | DUP-BUILDER |
| bridge_blocks_apply | PermissionError on apply_patch |
| bridge_rejects_unknown | error |
| mcp_sdk_tools | PASS con SDK / SKIP sin SDK |

## Resultado

| Check | Status |
|-------|--------|
| smoke sin SDK | **6/6** (sdk SKIP) |
| smoke con `.venv-mcp` | **6/6** (sdk PASS) |
| Cursor project config | `.cursor/mcp.json` → `ai-python-lab` |
| Setup | `bash scripts/setup_cursor_mcp.sh` |
| En `run_all_smokes.sh` | Sí (modo bridge; SDK opcional) |
