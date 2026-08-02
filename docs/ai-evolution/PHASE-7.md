# Fase 7 — Generación controlada de cambios

**Fecha:** 2026-07-30  
**Estado:** v1 entregada — recipes + allowlist + pipeline · smoke **4/4**  
**Precondiciones:** [Fase 5](PHASE-5.md) · [Fase 6](PHASE-6.md)

---

## Objetivo

Proponer (y solo con Gate 3 aplicar) parches **trazables**, allowlisteados y re-revisados. **Sin merge.**

---

## Flujo

```text
Plan Gate2 approved / recipe
   ↓
propose (validate paths)
   ↓
review_diff (block on high severity)
   ↓
awaiting_gate3  |  blocked
   ↓
apply --gate3-approved [--run-tests]
   ↓
(no git push / merge)
```

---

## Entregables

| Pieza | Path |
|-------|------|
| Allowlist | `tools/patches/v1/allowlist.json` |
| Recipes | `tools/patches/v1/recipes/` + `recipes.json` |
| Pipeline | `scripts/patch_pipeline.py` |
| Tool (propose only) | `propose_patch` in registry |
| Eval | `docs/ai-evolution/evals/009-patch-pipeline.md` |

---

## Comandos

```bash
python3 scripts/patch_pipeline.py propose --recipe bad-sleep-support
python3 scripts/patch_pipeline.py propose --recipe good-access-token-expired
python3 scripts/patch_pipeline.py apply --proposal-id <id> --gate3-approved --run-tests
python3 scripts/patch_pipeline.py smoke

python3 scripts/tools_runner.py invoke propose_patch --arg recipe=good-access-token-expired
```

Con workflow Gate2:

```bash
python3 scripts/patch_pipeline.py propose --recipe good-access-token-expired --from-run <run_id>
```

(`already_covered` plans are refused.)

---

## Smoke 4/4

| Check | Result |
|-------|--------|
| Bad recipe blocked (`STAB-SLEEP-CS`) | PASS |
| Good recipe → `awaiting_gate3` | PASS |
| Apply + `dotnet test` + restore | PASS |
| Refuse apply without Gate 3 | PASS |

---

## Restricciones v1

- Solo recipes allowlisteadas (no LLM libre escribiendo diffs aún).
- Prefijos: `labs/csharp-reqnroll-lab/src|tests/...`
- Deny: csproj, .env, bin/obj
- Apply exige `--gate3-approved`
- No push/merge

---

## Siguiente

Fase 8 agentes especializados (contratos Analyst/Planner/Builder/Reviewer ya semi-existen) **o** CI de smokes.  
LLM patch body = iteración posterior bajo el mismo allowlist/review/gate3.
