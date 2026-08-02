# Patches v1

Controlled patch generation (Phase 7).

| File | Role |
|------|------|
| `allowlist.json` | Allowed/denied paths |
| `recipes.json` | Recipe catalog |
| `recipes/*.diff` | Deterministic patch bodies |

```bash
python3 scripts/patch_pipeline.py smoke
```

See `docs/ai-evolution/PHASE-7.md`.
