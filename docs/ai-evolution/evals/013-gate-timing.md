# Eval 013 — Gate timing (machine + human waits)

**Fecha:** 2026-07-31 (human flow)  
**Command:** `python3 scripts/gate_timing.py smoke`  
**Contract:** `gate-timing.v1`  
**Plantilla:** [gate-timing-session.md](gate-timing-session.md)  
**Logs humanos:** [human-sessions/](human-sessions/)  
**Baseline:** [gate-timing-baseline.json](gate-timing-baseline.json)

## Objetivo

Separar lead time en machine vs human gates, con escenario guiado para sesiones reales.

## Criterios smoke

| Check | Esperado |
|-------|----------|
| duplicate_skip_propose | already_covered → propose skipped |
| token_propose_awaiting_gate3 | good recipe → awaiting_gate3 |
| record_human_waits | suma human_gate_ms |
| tools_runner_reachable | invoke ok |
| human_command_log | `human --scenario duplicate` escribe markdown |
| parse_duration | `1:30` / `2m` |

## Resultado

| Check | Status |
|-------|--------|
| `gate_timing.py smoke` | **6/6 PASS** |
| En `run_all_smokes.sh` | Sí |

## Sesión humana

```bash
python3 scripts/gate_timing.py human --scenario token-refresh --interactive --reviewer "TuNombre"
python3 scripts/gate_timing.py summarize
```
