# Fase 6 — Reviewer asistido (P1)

**Fecha:** 2026-07-30  
**Estado:** v1 entregada — taxonomía + fixtures UC-05–07 + `review_diff` · eval **3/3**  
**Precondiciones:** [Fase 5](PHASE-5.md)

---

## Objetivo

Usar reglas deterministas (+ agente opcional) para **revisar diffs** sin modificar código automáticamente.

---

## Entregables

| Entregable | Path |
|------------|------|
| Taxonomy | `knowledge/examples/review/taxonomy.md` |
| Fixtures UC-05–07 | `knowledge/examples/review/uc0*.diff` + `fixtures.json` |
| Reviewer script | `scripts/review_diff.py` |
| Registry tool | `review_diff` in `tools/registry/v1/registry.json` |
| Agent / prompt | `.github/agents/automation-reviewer.agent.md` |
| Eval | `docs/ai-evolution/evals/008-reviewer.md` |

---

## Comandos

```bash
python3 scripts/review_diff.py eval
python3 scripts/review_diff.py --fixture uc05 --json
python3 scripts/tools_runner.py invoke review_diff --arg fixture=uc06 --json
```

---

## Resultados v1

| Fixture | Expected | Result |
|---------|----------|--------|
| uc05 | `DUP-BUILDER` | PASS |
| uc06 | `STAB-SLEEP-CS` | PASS |
| uc07 | `XRAY-MISSING-TAG` | PASS |

---

## Criterios de salida

- [x] Taxonomía versionada
- [x] Diffs sintéticos UC-05–07
- [x] Tool read-only allowlisted
- [x] Eval 3/3
- [x] Agent reviewer (observes only)
- [ ] Integración PR bot / CI comment (después)
- [ ] Medición de falsos positivos en diffs reales

---

## Principio

El Reviewer **emite hallazgos**. No corrige solo. Gate humano decide.
