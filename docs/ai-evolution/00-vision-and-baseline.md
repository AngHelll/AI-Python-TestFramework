# Fase 0 — Visión y línea base

## Vision Statement

Evolucionar la práctica de automatización asistida por IA desde *few-shot prompting* aislado hacia una plataforma gobernada, contextual, medible y reutilizable — sin autonomía silenciosa y con decisión humana en gates críticos.

Este repositorio es el **laboratorio**:

| Capa | Ubicación | Rol |
|------|-----------|-----|
| Plataforma IA (prompts, agents, knowledge, workflows) | raíz Python + `knowledge/` + `docs/ai-evolution/` | Prototipar Context First → Analyst → Planner → Reviewer |
| Sujeto de evolución (espejo del stack laboral) | `labs/csharp-reqnroll-lab/` | C# · Reqnroll · xUnit · Builders · Validators |

El framework de trabajo real (C# / Reqnroll / xUnit) **no** se clona aquí. El lab C# es un gemelo reducido para evaluar retrieval, reutilización y planes técnicos transferibles.

## Alcance inicial (in / out)

### In scope (Fase 0 — cerrado)

- Fases 0–5 del roadmap en diseño: prompts estructurados, knowledge base, context retrieval manual, workflow de análisis/planificación.
- Human gates de análisis y plan.
- Dataset de evaluación con ≥5 historias.
- Mapeo de patrones Python ↔ C#.
- Dos ciclos plan → implementación en el lab (Token Refresh, Profile).

### Out of scope (aplazado)

- Agentes que hagan merge o publiquen.
- LangGraph / multi-agente completo / MCP productivo.
- Acceso real a Jira/XRay de producción.
- Reescritura del monorepo laboral.
- Tools read-only automatizadas (Fase 4).

## Proceso actual (as-is → to-be en lab)

**As-is (few-shot):** prompt + ejemplos → código variable sin evidencia.

**To-be (lab, post Fase 0):** solicitud → contexto/`knowledge` → Analyst → Gate 1 → Planner → Gate 2 → (opcional) implementación supervisada → catálogo actualizado.

**Éxito operativo (área):** ver [VALUE-AND-KPIS.md](VALUE-AND-KPIS.md) — eficiencia = fricción QA + contexto admin; agentico con gates; madurez = uso de agentes + métricas manuales; siguiente nivel ej. detector de cambios → plan de cobertura con autorización humana.

## Línea base (cerrada 2026-07-30)

Documento maestro: [`PHASE-0-COMPLETE.md`](PHASE-0-COMPLETE.md).

| Historia | Few-shot | Workflow | Notas |
|----------|----------|----------|-------|
| AUTH-TOKEN-REFRESH | 2 | 9 | Implementado |
| AUTH-DUPLICATE-BUILDER | Fallo esp. | PASS | Trampa reuso |
| USER-PROFILE-GET | 2 | 9 | Implementado |
| AUTH-LOGIN-NEG | 1 | 10 | Already covered |
| UI-LOGIN-FLAKY-RISKS | 0 | 9 | Riesgos flakiness |

Lab: `dotnet test` → **10 passed**.

## Criterio de salida Fase 0

- [x] Vision y alcance documentados
- [x] Casos de uso priorizados
- [x] Riesgos iniciales
- [x] Workflow Analyst→Planner especificado
- [x] Lab C# scaffold + Auth completo (login/refresh/profile)
- [x] ≥5 historias few-shot vs workflow
- [x] Cierre formal en `PHASE-0-COMPLETE.md`
