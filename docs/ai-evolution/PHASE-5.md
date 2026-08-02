# Fase 5 — Workflow ejecutable + tracing

**Fecha:** 2026-07-30  
**Estado:** v1 entregada — runner determinista + gates + smoke 3/3  
**Precondiciones:** [F4 tools](PHASE-4.md)

---

## Objetivo

Formalizar el flujo Analyst → tools → Planner → human gates con **estado persistido y auditable**, sin depender aún de un LLM ni de LangGraph.

El “Analyst/Planner” de este runner es un **context builder determinista** alimentado por `tools_runner`. Los agents de Cursor/Copilot siguen siendo la vía LLM; este script es el orquestador medible.

---

## Entregables

| Entregable | Path |
|------------|------|
| Run schema | `tools/workflow/v1/run.schema.json` |
| Sample requests | `tools/workflow/v1/samples/` |
| Orchestrator | `scripts/workflow_runner.py` |
| Live runs (gitignored) | `.forgeone/runs/workflow/` |
| Golden traces (committed) | `docs/ai-evolution/evals/runs/phase5-*.json` |

---

## Flujo

```text
Request JSON
   ↓
context: tools_runner (builder/validator/steps/features/clients/knowledge)
   ↓
analysis.v1 (deterministic)
   ↓
Gate 1 (pending | --auto-gates | workflow_runner gate)
   ↓
plan.v1 (deterministic)
   ↓
Gate 2
   ↓
delivered (NO patches)
```

---

## Comandos

```bash
# Auto gates (CI / smoke)
python3 scripts/workflow_runner.py start \
  --from tools/workflow/v1/samples/AUTH-DUPLICATE-BUILDER.json \
  --auto-gates

# Human gates
python3 scripts/workflow_runner.py start \
  --from tools/workflow/v1/samples/USER-PROFILE-GET.json
python3 scripts/workflow_runner.py gate --run-id <id> --gate 1 --decision approved --note "ok"
python3 scripts/workflow_runner.py gate --run-id <id> --gate 2 --decision approved --note "ok"
python3 scripts/workflow_runner.py show --run-id <id>

python3 scripts/workflow_runner.py smoke
```

---

## Criterios de salida

- [x] Schema `workflow-run.v1` con `tools_invoked`, gates, evidence, analysis, plan
- [x] Persistencia de runs
- [x] Integración real con tools registry (Fase 4)
- [x] Gate 1 / Gate 2 programáticos
- [x] Smoke: duplicate builder / already covered / interactive gates → **3/3**
- [x] Goldens committed bajo `evals/runs/`
- [ ] Sustituir producer determinista por LLM opcional (Fase 6+/SDK) — fuera de alcance
- [ ] Cronometraje humano de 3 runs reales — pendiente sesión

---

## Cómo combinar con Cursor agents

1. `workflow_runner.py start` (sin auto-gates) → obtiene evidence + draft analysis.
2. Revisar/editar analysis con agent `automation-analyst` si hace falta.
3. `gate --gate 1 --decision approved`
4. Revisar plan con `automation-planner` o aceptar el determinista.
5. `gate --gate 2 --decision approved`
6. Solo entonces implementar.

---

## Siguiente

- Reviewer asistido (P1 / UC-05–07) **o**
- Holguras: CI (`smoke` tools + retrieval + workflow), más seeds
- No MCP / LangGraph todavía
