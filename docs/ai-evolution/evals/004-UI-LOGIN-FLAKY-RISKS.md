# Eval run 004 — UI-LOGIN-FLAKY-RISKS (UC-04)

**Fecha:** 2026-07-30  
**Target:** `labs/csharp-reqnroll-lab` (+ principios aplicables a Python POM)  
**Request ID:** `UI-LOGIN-FLAKY-RISKS`  
**UC:** UC-04 Plan con riesgos de flakiness  
**Constraints:** plan only; historia UI hipotética sobre login

## 1. Entrada

> Automatizar login por UI en un portal lento. El equipo a veces usa waits fijos.
> Target preferido: documentar riesgos aunque el lab actual sea API-first.
> Restricción: no introducir flakiness.

## 2. Brazo A — Few-shot

```text
Page object con Thread.Sleep(2000) tras click.
Retry 5 veces engullendo cualquier Exception.
Assert débil: title.Contains("a") o IsNotNull genérico.
Static WebDriver compartido entre scenarios.
```

| Criterio | ¿Cumple? |
|----------|----------|
| Lista sleeps como riesgo | No (los introduce) |
| Evita shared state | No |
| Assertions fuertes | No |
| Evidencia anti-patterns | No |

**Score:** 0 · **Correcciones:** 6+

---

## 3. Brazo B — Analyst → Planner

### Evidencia

| Path | Reason |
|------|--------|
| `knowledge/anti-patterns/anti-patterns.md` | AP-03 sleep, AP-04 retries, AP-08 shared state |
| `knowledge/review-checklists/guardrails.md` | Checklist |
| `knowledge/patterns/approved-patterns.md` | Fake API / hooks por escenario |
| `Hooks/AuthHooks.cs` | Estado fresco por scenario (patrón bueno) |
| `prompts/context/best_practices.md` | Waits explícitos Python (si target raíz) |

### Analysis

```yaml
request_id: UI-LOGIN-FLAKY-RISKS
summary: >
  Historia UI de login en portal lento. El valor del run es forzar riesgos
  de estabilidad en el plan, no generar sleeps.
proposed_coverage:
  positive:
    - Login UI exitoso con wait explícito a elemento post-login
  negative:
    - Credenciales inválidas → mensaje visible (explicit wait)
  edge:
    - Timeout de página / elemento no encontrado debe fallar el test, no enmascararse
assumptions:
  - Lab C# hoy es API; UI sería extensión o espejo Python POM
open_questions:
  - ¿Selenium en lab C# o solo Python pages/?
out_of_scope:
  - Thread.Sleep fijos
  - Retries que tragan Assert
evidence:
  - path: knowledge/anti-patterns/anti-patterns.md
    reason: Catálogo de flakiness
```

**Gate 1:** APPROVED

### Plan

```yaml
request_id: UI-LOGIN-FLAKY-RISKS
reuse:
  builders: [LoginRequestBuilder]  # datos, aunque el canal sea UI
  validators: []
  steps: []
  pages_or_clients:
    - LoginPage (lab facade) o pages/login_page.py en Python
create_only_if_needed:
  - Solo si se aprueba UI real: locators + explicit waits — NUNCA Sleep
files_likely_affected:
  - (si Python) pages/login_page.py, features/login.feature
  - (si C# UI futuro) Pages/ + Feature nueva — requiere ADR
risks:
  - id: R-SLEEP
    severity: high
    note: Prohibido Thread.Sleep / time.sleep en camino feliz
  - id: R-RETRY-SWALLOW
    severity: high
    note: Retries no deben capturar AssertionException
  - id: R-SHARED-DRIVER
    severity: high
    note: Driver/API state por scenario (ver AuthHooks)
  - id: R-WEAK-ASSERT
    severity: medium
    note: Asserts deben anclar mensaje/error code, no presencia vaga
  - id: R-LAB-API-FIRST
    severity: low
    note: Preferir FakeAuthApi para evals deterministas; UI solo con justificación
implementation_steps:
  - Decidir target UI (Python existente) vs mantener API lab
  - Si UI: explicit waits + POM; reusar datos de Builder
  - Checklist guardrails en Gate 2
  - No mergear si el diff introduce Sleep
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
evidence:
  - path: knowledge/review-checklists/guardrails.md
    reason: Gate checklist
  - path: labs/.../Hooks/AuthHooks.cs
    reason: Patrón anti shared-state
```

**Gate 2:** APPROVED  
**Score:** 9

---

## 4. Scorecard

| Criterio | Few-shot | Workflow |
|----------|----------|----------|
| Marca sleeps como riesgo/prohibición | Fallo (los usa) | OK |
| Shared state / retries | Fallo | OK |
| Prepara Reviewer (UC-04) | Fallo | OK |

**Winner:** Workflow · **Lección:** el plan debe fallar gates si propone Sleep.
