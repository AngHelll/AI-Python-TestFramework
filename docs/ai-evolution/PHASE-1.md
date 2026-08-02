# Fase 1 — Prompt library (en curso / entregable v1)

**Fecha:** 2026-07-30  
**Estado:** v1 entregada — contratos + fragments + few-shots aprobados + skill/script de búsqueda  
**Precondición:** [Fase 0 cerrada](PHASE-0-COMPLETE.md)

---

## Objetivo

Convertir prompts ad-hoc en **contratos repetibles** con forma de salida estable, fragmentos compartidos y ejemplos humanos aprobados.

---

## Entregables

| Entregable | Path |
|------------|------|
| Contracts `analysis.v1` / `plan.v1` | `prompts/contracts/` |
| Fragments (anti-patterns, gates, load order) | `prompts/fragments/` |
| Library index | `prompts/library/README.md` |
| Approved few-shots FS-01…03 | `prompts/examples/approved/` |
| Prompts/agents actualizados | `.github/prompts/automation-*`, `.github/agents/automation-*` |
| Skill búsqueda | `.github/skills/find-existing-components/` |
| Script read-only | `scripts/find_existing_components.py` |
| Retrieval seeds | `knowledge/examples/retrieval-seeds.md` |

---

## Cómo usar en un run

1. Invocar Analyst con `.github/prompts/automation-analyst.prompt.md`.
2. Exigir YAML conforme a `analysis.v1`.
3. Gate 1 con `prompts/fragments/gate-criteria.md`.
4. Planner + `plan.v1` + skill/script de componentes.
5. Gate 2; solo entonces implementar.

---

## Criterios de salida Fase 1

- [x] Contratos versionados analysis/plan
- [x] Fragments reutilizables
- [x] ≥3 few-shots aprobados enlazados a goldens/evals
- [x] Prompts/agents referencian contratos
- [x] Al menos una capacidad de búsqueda read-only (script + skill)
- [ ] Medir variación de formato en 3 runs humanos (pendiente sesión real)
- [ ] Checklist de calidad de prompts firmado por el equipo (pendiente)

---

## Fuera de esta entrega

- MCP server
- Orquestación Semantic Kernel / Agents SDK
- Reviewer automático en PR
- Cambiar contratos a v2 sin necesidad
