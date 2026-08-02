# Fase 8 — Agentes especializados

**Fecha:** 2026-07-30  
**Estado:** v1 — contracts + handoffs + Builder agent · CI smokes añadido  
**Precondiciones:** Fases 5–7

---

## Objetivo

Separar Analyst / Planner / Builder / Reviewer con límites explícitos y handoffs trazables.

---

## Entregables

| Pieza | Path |
|-------|------|
| Contracts | `knowledge/agents/contracts.md` |
| Handoffs | `knowledge/agents/handoffs.md` |
| Builder agent/prompt | `.github/agents/automation-builder.agent.md` |
| CI smokes | `.github/workflows/ai-evolution-smokes.yml` |
| Local runner | `scripts/run_all_smokes.sh` |

---

## Roles (resumen)

| Rol | Escribe código? | Aplica patch? | Merge? |
|-----|-----------------|---------------|--------|
| Analyst | No | No | No |
| Planner | No | No | No |
| Builder | Propone recipe/diff | No (salvo Gate 3 humano) | No |
| Reviewer | No | No | No |

---

## Criterios de salida

- [x] Matriz de responsabilidades
- [x] Handoffs documentados
- [x] Builder agent (propose-only)
- [x] CI / script de smokes F4–F7
- [x] Sub-reviewers (Architecture/Stability/XRay/Security) — Stability/XRay/Security v1 via `--category`
- [ ] LLM Builder emitiendo diff libre bajo allowlist — posterior

---

## Siguiente

Fase 9 (MCP) solo cuando las tools estén estables y haya ≥2 clientes.  
Antes: ampliar recipes/seeds o sub-reviewers.
