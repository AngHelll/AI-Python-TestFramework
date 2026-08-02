# Eval 012 — .NET transfer POC (orchestration aledaño)

**Fecha:** 2026-07-31 (actualizado)  
**Repo:** `ai-automation-orchestration` (sibling de este lab)  
**ADR:** [ADR-002](../../../knowledge/decisions/ADR-002-orchestration.md)  
**Doc:** [PHASE-9-TRANSFER-POC.md](../PHASE-9-TRANSFER-POC.md)

## Objetivo

Probar que un host .NET puede:

1. Invocar tools allowlisteadas del lab
2. Exponerlas como plugin Semantic Kernel
3. (Opcional) Chat + function calling
4. Emitir handoffs YAML `analysis.v1` / `plan.v1`
5. Proponer patches via recipes y **negar apply** sin Gate 3

## Criterios

| # | Criterio | Cómo | Esperado |
|---|----------|------|----------|
| 1 | Gateway find builder | `smoke` | PASS |
| 2 | Review UC-05 | review_diff uc05 | DUP-BUILDER |
| 3 | SK plugin | sk-invoke | PASS sin LLM |
| 4 | Chat opcional | chat-smoke | PASS / **SKIP** |
| 5 | analysis.v1 / plan.v1 | contracts-smoke | PASS |
| 6 | Skip propose si already_covered | build-smoke | PASS |
| 7 | Good recipe → awaiting_gate3 | build-smoke | PASS |
| 8 | Bad recipe blocked | build-smoke | PASS |
| 9 | Refuse apply sin Gate3 | build-smoke + smoke | PASS |
| 10 | Lab `patch_pipeline smoke 4/4` | build-smoke | PASS |

## Resultado

| Check | Status |
|-------|--------|
| smoke (gateway+contratos+builder gates, chat SKIP) | **PASS** (2026-07-31) |
| contracts-smoke | **PASS** |
| build-smoke (5/5) | **PASS** |
| chat-smoke con LLM | no ejecutado (sin credenciales) |

## Notas

- Artefactos YAML: `ai-automation-orchestration/artifacts/` (gitignored)
- Proposals viven en el lab: `.forgeone/runs/patches/`
- No forma parte de `scripts/run_all_smokes.sh` del lab (otro repo)
