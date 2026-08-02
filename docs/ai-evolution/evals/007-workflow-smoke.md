# Eval — Workflow runner smoke (Phase 5)

**Fecha:** 2026-07-30  
**Command:** `python3 scripts/workflow_runner.py smoke`  
**Result:** **3/3 PASS**

| Case | Expectation | Result |
|------|-------------|--------|
| AUTH-DUPLICATE-BUILDER | `already_covered`, reuse LoginRequestBuilder, empty create | PASS |
| AUTH-LOGIN-NEG | already covered + gates approved | PASS |
| USER-PROFILE-GET | awaiting_gate1 → gate1 → gate2 → completed | PASS |

Golden JSON: [`runs/`](runs/) (`phase5-*.json`).

See [PHASE-5.md](../PHASE-5.md).
