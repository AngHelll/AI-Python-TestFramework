# Metrics v1

| Pieza | Path |
|-------|------|
| Schema | `gate-timing.schema.json` (`gate-timing.v1`) |
| Runner | `python3 scripts/gate_timing.py` |
| Sessions | `.forgeone/runs/metrics/` (gitignored) |
| Human template | `docs/ai-evolution/evals/gate-timing-session.md` |
| Eval | `docs/ai-evolution/evals/013-gate-timing.md` |

```bash
python3 scripts/gate_timing.py smoke
python3 scripts/gate_timing.py human --scenario token-refresh --interactive --reviewer "TuNombre"
python3 scripts/gate_timing.py summarize
```
