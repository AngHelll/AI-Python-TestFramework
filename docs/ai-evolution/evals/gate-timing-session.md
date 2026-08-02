# Plantilla — sesión de medición humana de gates

Contrato: `gate-timing.v1` · Eval: [013-gate-timing.md](013-gate-timing.md) · Logs: [human-sessions/](human-sessions/)

## Flujo recomendado (3–5 min)

```bash
# 1) Ver escenarios
python3 scripts/gate_timing.py scenarios

# 2a) Interactivo (cronómetro en mano)
python3 scripts/gate_timing.py human --scenario token-refresh --interactive --reviewer "TuNombre"

# 2b) O con tiempos ya medidos
python3 scripts/gate_timing.py human --scenario duplicate \
  --reviewer "TuNombre" \
  --gate1-sec 90 --gate2-sec 60 --gate3-sec 0 \
  --note "pair 2026-07-31"

# 3) Promedios
python3 scripts/gate_timing.py summarize
```

Durante el paso 2 el harness:

1. Corre la parte **máquina** (context → analysis → plan → propose si aplica)
2. Escribe un bundle legible en `.forgeone/runs/metrics/<session_id>/analysis.v1.json` + `plan.v1.json`
3. Te pide (o recibe) tiempos de Gate 1/2/3
4. Guarda JSON + markdown en `docs/ai-evolution/evals/human-sessions/`

## Escenarios

| id | Request | Gate 3 |
|----|---------|--------|
| `duplicate` | AUTH-DUPLICATE-BUILDER | 0 (already_covered) |
| `token-refresh` | AUTH-TOKEN-REFRESH + recipe | leer proposal, **sin apply** |
| `login-neg` | AUTH-LOGIN-NEG | 0 (already covered) |

## Qué cronometrar

| Gate | Incluye | No incluye |
|------|---------|------------|
| 1 | Leer analysis + decidir | Tiempo del LLM generando analysis |
| 2 | Leer plan + reuse/create | Implementación |
| 3 | Leer proposal/review | `apply` / `dotnet test` |

Duraciones aceptadas: `90`, `90s`, `1:30`, `2m`.

## Separación

- **machine_ms** — automatizable
- **human_gate_ms** — solo decisión humana
- **wall_ms** — proxy de lead time

Si usaste chat LLM, anótalo en `--note` (no lo mezcles en los gates).

## Smoke

```bash
python3 scripts/gate_timing.py smoke
```
