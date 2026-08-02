# Fase 2–3 — Context / retrieval (baseline)

**Fecha:** 2026-07-30  
**Estado:** Baseline v0 entregada — seeds + harness + recall@3/5 = 1.0  
**Precondiciones:** [Fase 0](PHASE-0-COMPLETE.md) · [Fase 1](PHASE-1.md)

---

## Objetivo

Recuperar contexto del repo de forma **repetible y medible**, no solo “el modelo se acuerda”.

---

## Entregables

| Entregable | Path |
|------------|------|
| Seeds machine-readable | `knowledge/examples/retrieval-seeds.json` |
| Seeds doc | `knowledge/examples/retrieval-seeds.md` |
| Finder (ranking + knowledge + JSON) | `scripts/find_existing_components.py` |
| Eval harness | `scripts/eval_retrieval.py` |
| Baseline JSON | `docs/ai-evolution/evals/retrieval-baseline.json` |
| Skill | `.github/skills/find-existing-components/SKILL.md` |

---

## Cómo correr

```bash
# Búsqueda manual
python3 scripts/find_existing_components.py --target csharp --terms RefreshToken,refresh --limit 5
python3 scripts/find_existing_components.py --target knowledge --query sleep --json

# Eval (debe salir 8/8)
python3 scripts/eval_retrieval.py --k 5
python3 scripts/eval_retrieval.py --k 3
```

Exit code `0` = todos los expected_paths aparecen en top-k.

---

## Resultados baseline (2026-07-30)

| Métrica | Valor |
|---------|-------|
| Casos | 8 |
| recall@5 | **1.0** (8/8) |
| recall@3 | **1.0** (8/8) |
| Ruido típico @5 | 1–4 paths extra (aceptable en v0) |

Hallazgos de diseño:

1. Buscar en `docs/ai-evolution/evals/` ensuciaba knowledge → **excluido** del target `knowledge`.
2. Substring `refresh` priorizaba `RefreshTokenData` sobre `AuthApiClient` → bonus por **word-boundary** + boost de path.
3. Queries libres necesitan `terms` explícitos en seeds (el Planner debe preferir términos de catálogo).

---

## Criterios de salida Fase 2–3 (v0)

- [x] Dataset de seeds versionado (JSON)
- [x] Harness automatizado
- [x] recall@5 = 1.0 en seeds v0.1.0
- [x] recall@3 = 1.0 tras tuning de ranking
- [x] Documentado ruido residual
- [ ] Ampliar a ≥15 seeds (Python + más Auth)
- [ ] Salida JSON consumible por tool registry (Fase 4)

---

## Uso en Analyst / Planner

1. Traducir pedido → `terms` (o usar seeds cercanas).
2. Ejecutar finder con `--limit 5`.
3. Pegar paths en `evidence` del contrato `analysis.v1` / `plan.v1`.
4. No marcar `searched_before_create: true` sin haber corrido búsqueda.

---

## Fuera de alcance aún

- Embeddings / vector DB
- MCP tool wrapping
- CI gate obligatorio (recomendado después de ≥15 seeds)
