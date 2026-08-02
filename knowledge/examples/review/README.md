# Review fixtures

| Id | Category | Expected |
|----|----------|----------|
| uc05 | duplication | DUP-BUILDER |
| uc06 | stability | STAB-SLEEP-CS |
| uc06b | stability | STAB-SLEEP-PY |
| uc07 | xray | XRAY-MISSING-TAG |
| uc-sec | security | SEC-SECRET |

```bash
python3 scripts/review_diff.py eval
python3 scripts/review_diff.py eval --category stability
```

Taxonomy: [taxonomy.md](taxonomy.md)
