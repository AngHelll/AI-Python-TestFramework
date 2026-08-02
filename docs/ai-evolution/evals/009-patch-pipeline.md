# Eval 009 — Controlled patch pipeline

**Fecha:** 2026-07-30  
**Command:** `python3 scripts/patch_pipeline.py smoke`  
**Result:** **4/4 PASS**

| Check | Expectation |
|-------|-------------|
| bad-sleep-support | status=blocked, code STAB-SLEEP-CS |
| good-access-token-expired | status=awaiting_gate3, review clean |
| apply + tests + restore | dotnet test pass, tree restored |
| apply without gate3 | refused |

Baseline: [patch-pipeline-baseline.json](patch-pipeline-baseline.json)  
Docs: [PHASE-7.md](../PHASE-7.md)
