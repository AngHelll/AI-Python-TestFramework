# MCP v1 — lab tools wrapper

**ADR-002:** Envolver `tools_runner`, no reemplazar allowlists.  
**Clientes:** Cursor/IDE + host .NET (`LabToolGateway`) → justifica MCP.

## Piezas

| Pieza | Path |
|-------|------|
| Bridge (sin SDK) | `scripts/lab_mcp_bridge.py` |
| Stdio server | `scripts/mcp_lab_server.py` |
| Launcher | `scripts/mcp_lab_server_launch.sh` |
| Setup Cursor | `scripts/setup_cursor_mcp.sh` |
| Project config | `.cursor/mcp.json` → server **`ai-python-lab`** |
| Smoke | `scripts/mcp_lab_smoke.py` |
| Deps | `requirements-mcp.txt` + `.venv-mcp/` |

## Setup (una vez)

```bash
bash scripts/setup_cursor_mcp.sh
```

Luego en Cursor: **Settings → MCP → refresh** (o reiniciar). Debe aparecer `ai-python-lab` con:

- `list_lab_tools`
- `invoke_lab_tool`
- `choose_gate2_recipe`

## Tools

- `list_lab_tools` — catálogo registry
- `invoke_lab_tool` — delega a `tools_runner.invoke`
- `choose_gate2_recipe` — post–Gate2 chooser allowlisted (propose opcional; **nunca apply**)

**No** expone apply/merge/push. Gate 3: `patch_pipeline.py apply --gate3-approved`.

```bash
bash scripts/demo_gate2_recipe_flow.sh
```

Eval: `docs/ai-evolution/evals/014-mcp-lab.md` · `015-gate2-recipe-chat.md`
