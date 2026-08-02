# Casos de uso priorizados

Prioridad: P0 = primer sprint de evals · P1 = siguiente · P2 = más adelante.

## P0 — Análisis y planificación (sin modificar código)

| ID | Caso de uso | Entrada | Salida esperada | Por qué |
|----|-------------|---------|-----------------|---------|
| UC-01 | Nueva automatización login API | Historia + dominio Auth | Plan + builders/validators a reutilizar | Caso canónico del lab C# |
| UC-02 | Extender feature BDD existente | Feature path + cambio | Steps reutilizables + riesgos | Reuse Before Create |
| UC-03 | Detectar cobertura existente | Jira stub / descripción | Automatizaciones similares | Evita duplicar escenarios |
| UC-04 | Plan con riesgos de flakiness | Historia UI | Sleeps, waits, shared state en riesgos | Prepara Reviewer |

## P1 — Reviewer asistido

| ID | Caso de uso | Estado |
|----|-------------|--------|
| UC-05 | Builder duplicado | **Done** — fixture `uc05` / `DUP-BUILDER` |
| UC-06 | Thread.Sleep | **Done** — fixture `uc06` / `STAB-SLEEP-CS` |
| UC-07 | Tags XRay faltantes | **Done** — fixture `uc07` / `XRAY-MISSING-TAG` |

Ver `docs/ai-evolution/PHASE-6.md`.

## P2 — Generación controlada

| ID | Caso de uso | Estado |
|----|-------------|--------|
| UC-08 | Patch bajo plan/recipe + Gate 3 | **Done v1** — `patch_pipeline.py` |
| UC-09 | Compilar/tests dirigidos | **Done v1** — `dotnet test` en apply |

Ver `docs/ai-evolution/PHASE-7.md`.

## Historias de evaluación (golden set v0)

| Historia | Eval | Estado código |
|----------|------|---------------|
| AUTH-LOGIN-OK | (sanity lab) | Automatizado |
| AUTH-LOGIN-NEG | [003](evals/003-AUTH-LOGIN-NEG-coverage.md) | Ya existía — workflow dice no crear |
| AUTH-LOCKOUT | (sanity lab) | Automatizado |
| AUTH-TOKEN-REFRESH | [001](evals/001-AUTH-TOKEN-REFRESH.md) | Implementado post Gate 2 |
| USER-PROFILE-GET | [002](evals/002-USER-PROFILE-GET.md) | Implementado post Gate 2 |
| AUTH-DUPLICATE-BUILDER | 001 trampa | Policy PASS |
| UI-LOGIN-FLAKY-RISKS | [004](evals/004-UI-LOGIN-FLAKY-RISKS.md) | Plan only (UC-04) |

Goldens humanos: `knowledge/examples/`.
