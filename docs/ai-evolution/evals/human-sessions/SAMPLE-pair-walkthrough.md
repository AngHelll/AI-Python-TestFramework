# Human gate session — SAMPLE (pair walkthrough)

Ejemplo **ilustrativo** (no es una medición real). Sirve de formato esperado.

- **session_id:** `SAMPLE-human-walkthrough`
- **request_id:** `AUTH-TOKEN-REFRESH`
- **reviewer:** Pair (ejemplo)
- **note:** Formato de referencia — reemplazar con sesiones reales

## Totals

| machine_ms | human_gate_ms | wall_ms |
|------------|---------------|---------|
| ~15 | 210000 | ~210015 |

## Human gates (ms)

| Gate 1 | Gate 2 | Gate 3 |
|--------|--------|--------|
| 120000 (2m) | 60000 (1m) | 30000 (30s) |

## Checklist

- [x] Gate1: leer summary + evidence de FakeAuthApi / TokenRefresh
- [x] Gate2: reuse vs create_only_if_needed; searched_before_create
- [x] Gate3: proposal awaiting_gate3; review clean; NO apply en la sesión de medición

## Comando equivalente

```bash
python3 scripts/gate_timing.py human --scenario token-refresh \
  --reviewer "Pair" \
  --gate1 2m --gate2 1m --gate3 30s \
  --note "ejemplo de formato"
```
