# Prompt contracts — v1.0.0

**Phase:** 1 (Prompt library formal)  
**Status:** Active  
**Aligned with:** `docs/ai-evolution/workflow-analyst-planner.md`

| Contract | File | Used by |
|----------|------|---------|
| Analysis output | `analysis.v1.yaml` | Analyst / Gate 1 |
| Plan output | `plan.v1.yaml` | Planner / Gate 2 |
| Shared fragments | `../fragments/` | Both |

## Versioning rules

- Breaking change to required fields → bump major (`analysis.v2.yaml`).
- Optional fields / clarifications → bump minor in this README + changelog note.
- Keep prior major files until evals migrate (do not delete v1 while evals 001–004 reference it).

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-07-30 | Initial contracts from workflow §6 |
