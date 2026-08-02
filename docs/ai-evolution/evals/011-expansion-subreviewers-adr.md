# Eval 011 — Seeds≥15, sub-reviewers, ADR-002

**Fecha:** 2026-07-30

| Check | Result |
|-------|--------|
| Retrieval seeds v0.2 | **16/16** @k=5 and @k=3 |
| Reviewer fixtures | **5/5** (uc05, uc06, uc06b, uc07, uc-sec) |
| Sub-reviewer `--category stability` | 2/2 |
| Sub-reviewer `--category security` | 1/1 |
| Recipe `good-refresh-token-expired` | propose → awaiting_gate3 |
| ADR-002 orchestration | `knowledge/decisions/ADR-002-orchestration.md` |
| Sub-reviewer agents | stability / xray / security |

```bash
python3 scripts/eval_retrieval.py --k 5
python3 scripts/review_diff.py eval
bash scripts/run_all_smokes.sh
```
