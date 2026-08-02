# ADR-002: Orquestación de agentes (lab vs transferencia laboral)

## Estado

Aceptado (provisional) — 2026-07-30 · actualizado 2026-07-31  

**POC .NET:** `ai-automation-orchestration` — gateway, SK `lab`, chat opcional, contratos YAML, Builder/Gate3.  
**MCP v1:** `scripts/mcp_lab_server.py` envuelve `tools_runner` (bridge + stdio). Eval [014](../../docs/ai-evolution/evals/014-mcp-lab.md).

## Contexto

El lab ya tiene tools, workflow determinista, reviewer y patch pipeline en Python/Cursor. El framework de trabajo es C# / Reqnroll. Hay ≥2 caminos a las mismas tools (scripts/Cursor + host .NET).

## Decisión

1. **Lab:** Cursor + scripts + agents; registry/`tools_runner` como API estable.
2. **Transfer .NET:** Semantic Kernel plugins tipados sobre el mismo gateway (POC hecho).
3. **MCP:** Wrapper stdio de `tools_runner` (`list_lab_tools` / `invoke_lab_tool`). No replace allowlists. No apply vía MCP.
4. **OpenAI Agents SDK / LangGraph:** Solo con necesidad clara de handoffs/checkpoints fuera de este stack.

## Consecuencias

- Clientes nuevos deben llamar bridge/MCP/`tools_runner`, no reimplementar búsqueda.
- Gate 3 apply permanece en `patch_pipeline.py --gate3-approved`.
- El **LLM es pluggable** (Copilot, Cursor, API, local OpenAI-compatible): `docs/ai-evolution/LLM-PORTABILITY.md`.
- Workflow humano Copilot: `docs/ai-evolution/COPILOT-RUNBOOK.md`.

## Revisión

Reabrir si un host exige bypassear `tools_runner`, auto-merge, o contratos incompatibles con `analysis.v1` / `plan.v1`.
