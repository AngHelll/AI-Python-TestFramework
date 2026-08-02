# Known issues / trampas de eval

| ID | Descripción | Expectativa / estado |
|----|-------------|----------------------|
| KI-01 | TokenRefresh @ignore sin steps | **RESUELTO** — implementado post Gate 2 |
| KI-02 | Pedir “nuevo builder de login” | Debe citar `LoginRequestBuilder` — PASS en eval 001 |
| KI-03 | GetProfile sin feature | **RESUELTO** — `Profile.feature` + `UserProfileValidator` |
| KI-04 | Pedir login negativo “nuevo” | Debe detectar `@AUTH-LOGIN-NEG` existente — eval 003 |
| KI-05 | Historia UI con sleeps | Plan debe prohibir Sleep y listar riesgos — eval 004 |

## Deuda deliberada (post Fase 0)

- Sin Semantic Kernel / Agents SDK / MCP / LangGraph.
- Sin tools read-only automatizadas (búsqueda manual + agents).
- Sin Jira/XRay reales (tags sintéticos `@AUTH-*` / `@USER-*`).
- Reviewer P1 (UC-05–07) no iniciado.
- Tiempos de Gate humano aún estimados, no cronometrados en sesión real.
