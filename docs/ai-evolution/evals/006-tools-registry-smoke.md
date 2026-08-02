# Eval / smoke — Tool registry

**Fecha:** 2026-07-30  
**Command:** `python3 scripts/tools_runner.py smoke`  
**Result:** **6/6 PASS**

| Check | Result |
|-------|--------|
| find_existing_builder → LoginRequestBuilder | PASS |
| validate_naming rejects bad builder name | PASS |
| unknown tool rejected | PASS |
| target allowlist (builder≠knowledge) | PASS |
| detect_forbidden_patterns runs | PASS |
| find_knowledge → component-catalog | PASS |

Regression: `python3 scripts/eval_retrieval.py --k 5` → 8/8.

See [PHASE-4.md](../PHASE-4.md).
