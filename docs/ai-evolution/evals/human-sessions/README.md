# Human gate sessions

Logs generados por `python3 scripts/gate_timing.py human …`.

- JSON crudo: `.forgeone/runs/metrics/<session_id>.json` (gitignored)
- Markdown aquí: `YYYY-MM-DD-<session_id>.md` (commiteable si quieres historial de equipo)

## Cómo aportar una sesión

1. Sigue [gate-timing-session.md](../gate-timing-session.md)
2. Commit del `.md` generado (opcional; útil para baselines humanas)
3. No commits de secretos ni de `.forgeone/runs/`

## Resumen

```bash
python3 scripts/gate_timing.py summarize
```
