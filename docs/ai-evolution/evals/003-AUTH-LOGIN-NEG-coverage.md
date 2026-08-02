# Eval run 003 — AUTH-LOGIN-NEG (cobertura existente / UC-03)

**Fecha:** 2026-07-30  
**Target:** `labs/csharp-reqnroll-lab`  
**Request ID:** `AUTH-LOGIN-NEG`  
**UC:** UC-03 Detectar cobertura existente  
**Constraints:** plan only — ¿hay que automatizar login fallido?

## 1. Entrada

> Necesitamos automatizar el caso de login con credenciales inválidas y verificar mensaje de error. Dominio Auth, lab C#.

## 2. Brazo A — Few-shot

```text
Crear LoginNegative.feature nueva.
Nuevo InvalidLoginBuilder + ErrorMessageValidator.
Steps nuevos sin mirar Login.feature.
```

| Criterio | ¿Cumple? |
|----------|----------|
| Encuentra `@AUTH-LOGIN-NEG` existente | No |
| Reutiliza `LoginRequestBuilder.AsInvalidUser` | No |
| Reutiliza `LoginResponseValidator.ShouldFailWith` | No |
| Evidencia | No |

**Score:** 1 · **Correcciones:** 5+

---

## 3. Brazo B — Analyst → Planner

### Evidencia

| Path | Reason |
|------|--------|
| `Features/Login.feature` | Scenario `@AUTH-LOGIN-NEG` ya automatizado |
| `Steps/LoginSteps.cs` | `AsInvalidUser` + fail assertions |
| `Builders/LoginRequestBuilder.cs` | `AsInvalidUser` |
| `Validators/LoginResponseValidator.cs` | `ShouldFailWith` |
| `knowledge/framework/component-catalog.md` | Inventario |

### Analysis

```yaml
request_id: AUTH-LOGIN-NEG
summary: >
  La cobertura solicitada YA existe en Login.feature (@AUTH-LOGIN-NEG).
  No se requiere nueva automatización; como máximo documentación o tag XRay.
proposed_coverage:
  positive: []
  negative:
    - Login inválido → INVALID_CREDENTIALS + mensaje (YA CUBIERTO)
  edge: []
assumptions:
  - El pedido es cobertura funcional, no un cambio de contrato
open_questions:
  - ¿Se pide un escenario Outline adicional de mensajes localizados?
out_of_scope:
  - Reimplementar login negativo
evidence:
  - path: labs/.../Features/Login.feature
    reason: Scenario Failed login with invalid credentials
```

**Gate 1:** APPROVED — “no build” es un resultado válido.

### Plan

```yaml
request_id: AUTH-LOGIN-NEG
reuse:
  builders: [LoginRequestBuilder]
  validators: [LoginResponseValidator]
  steps: [LoginSteps]
  pages_or_clients: [LoginPage, AuthApiClient]
create_only_if_needed: []
files_likely_affected: []
risks:
  - id: R-DUPLICATE-FEATURE
    severity: high
    note: Crear LoginNegative.feature duplicaría cobertura y deuda
implementation_steps:
  - Confirmar escenario existente con dotnet test (filtro login/negative)
  - Si el negocio pide XRay key, solo añadir tag — sin lógica nueva
  - Rechazar ticket de “nueva automatización” o marcar como Already Covered
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
evidence:
  - path: labs/.../Features/Login.feature
    reason: Cobertura existente
```

**Gate 2:** APPROVED (plan = no crear)  
**Score:** 10

---

## 4. Scorecard

| Criterio | Few-shot | Workflow |
|----------|----------|----------|
| Detecta cobertura existente | Fallo | OK |
| Evita duplicación | Fallo | OK |
| create_only_if_needed vacío | Fallo | OK |

**Winner:** Workflow · **Lección:** Analyst puede concluir “ya cubierto”.
