# Fase 0 — Cierre

**Fecha de cierre:** 2026-07-30  
**Estado:** Completada (criterios de salida cumplidos)  
**Ámbito:** Laboratorio dual en `AI-Python-TestFramework` (no el monorepo laboral)

---

## 1. Qué se buscaba

Pasar de few-shot aislado a una práctica medible: contexto, Analyst → Planner, human gates, evidencia, y un sujeto C# parecido al stack de trabajo — **sin autonomía de merge**.

---

## 2. Entregables

| Entregable | Ubicación |
|------------|-----------|
| Visión y alcance | [`00-vision-and-baseline.md`](00-vision-and-baseline.md) |
| Casos de uso | [`01-use-cases.md`](01-use-cases.md) |
| Riesgos | [`02-risks.md`](02-risks.md) |
| Contrato workflow | [`workflow-analyst-planner.md`](workflow-analyst-planner.md) |
| Knowledge base v0 | [`../../knowledge/`](../../knowledge/) |
| Lab C# Reqnroll/xUnit | [`../../labs/csharp-reqnroll-lab/`](../../labs/csharp-reqnroll-lab/) |
| Agents / prompts | `.github/agents/automation-*`, `.github/prompts/automation-*` |
| Rúbrica de evals | [`evals/RUBRIC.md`](evals/RUBRIC.md) |
| Evals golden | [`evals/`](evals/) (001–004) |

---

## 3. Línea base ≥5 historias

| # | Historia / UC | Eval | Few-shot | Workflow | Código |
|---|---------------|------|----------|----------|--------|
| 1 | AUTH-TOKEN-REFRESH | [001](evals/001-AUTH-TOKEN-REFRESH.md) | 2 | 9 | Implementado (6→10 tests con profile) |
| 2 | AUTH-DUPLICATE-BUILDER | 001 (trampa) | Fallo esp. | PASS | N/A (policy) |
| 3 | USER-PROFILE-GET | [002](evals/002-USER-PROFILE-GET.md) | 2 | 9 | Implementado |
| 4 | AUTH-LOGIN-NEG (cobertura) | [003](evals/003-AUTH-LOGIN-NEG-coverage.md) | 1 | 10 | Ya existía — no crear |
| 5 | UI-LOGIN-FLAKY-RISKS (UC-04) | [004](evals/004-UI-LOGIN-FLAKY-RISKS.md) | 0 | 9 | Plan only (riesgos) |

**Promedio workflow ≈ 9 · promedio few-shot ≈ 1–2** en planes comparables.

---

## 4. Lab C# — estado verificable

```bash
cd labs/csharp-reqnroll-lab && dotnet test
# Esperado: 10 passed (login 3 + refresh 3 + profile 4)
```

| Área | Componentes |
|------|-------------|
| Builders | `LoginRequestBuilder` |
| Validators | `LoginResponseValidator`, `UserProfileValidator` |
| Clients | `AuthApiClient` / `FakeAuthApi` |
| Support | `RefreshTokenData`, `AccessTokenData` |
| Features | `Login`, `TokenRefresh`, `Profile` |

---

## 5. Decisiones que sostienen el cierre

1. **ADR-001** — laboratorio dual Python (plataforma) + C# (sujeto).
2. Gates simulados en evals son **explícitos**; merge sigue humano.
3. “Already covered” (eval 003) cuenta como éxito del Analyst.
4. No se adoptó aún Semantic Kernel / Agents SDK / MCP / LangGraph (criterio roadmap §15: evidencia primero).

---

## 6. Límites conscientes (no son fallos de Fase 0)

| Fuera de alcance ahora | Dónde vive después |
|------------------------|--------------------|
| Tools read-only automatizadas | Fase 4 |
| Reviewer en PR | Fase 6 / P1 UC-05–07 |
| Orquestación SK / Agents SDK | Tras más evals + ADR |
| Jira/XRay reales | Stubs → Fase 4+ |
| Clonar framework laboral | Nunca en este repo |

---

## 7. Cómo retomar (humano)

1. Leer este cierre + [`NEXT-STEPS.md`](NEXT-STEPS.md).
2. Para nueva historia: agents `automation-analyst` → Gate 1 → `automation-planner` → Gate 2.
3. Comparar con golden en `knowledge/examples/` y catálogo.
4. Solo entonces implementar (como Token Refresh y Profile).

---

## 8. Criterios de salida — checklist final

- [x] Problema medible y caso de uso delimitado
- [x] Vision / UC / riesgos
- [x] Workflow Analyst→Planner especificado
- [x] Knowledge v0 + mapeo Python↔C#
- [x] Lab C# ejecutable
- [x] ≥5 historias few-shot vs workflow documentadas
- [x] Al menos un ciclo plan aprobado → implementación (Refresh + Profile)
