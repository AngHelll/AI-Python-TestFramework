# Eval run — Retrieval baseline

**Fecha:** 2026-07-30  
**Harness:** `scripts/eval_retrieval.py`  
**Seeds:** `knowledge/examples/retrieval-seeds.json` v0.1.0  
**Artifact:** [retrieval-baseline.json](retrieval-baseline.json)

## Summary

| k | recall | Result |
|---|--------|--------|
| 5 | 8/8 = 1.0 | PASS |
| 3 | 8/8 = 1.0 | PASS |

See [PHASE-2-3.md](../PHASE-2-3.md) for ranking notes and residual noise.

## Reproduce

```bash
python3 scripts/eval_retrieval.py --k 5
python3 scripts/eval_retrieval.py --k 3
```
