# Eval run 002 — USER-PROFILE-GET

**Fecha:** 2026-07-30  
**Target:** `labs/csharp-reqnroll-lab`  
**Request ID:** `USER-PROFILE-GET`  
**Dominio:** Auth / User  
**Constraints:** plan only en la eval original; **implementado** el mismo día tras Gate 2.

## 1. Entrada

> Como cliente API quiero obtener el perfil del usuario autenticado (`username`, `displayName`, `role`) usando un access token válido.  
> Negativos: token vacío o no prefijado `lab-token-*` → sin perfil (null / no autorizado).

## 2. Brazo A — Few-shot ingenuo

```text
Crear UserProfileService + UserProfileRequestBuilder + UserProfileValidator.
Nueva feature Profile.feature desde cero.
HttpClient real a /api/profile.
Asserts en steps; posible retry/sleep si “el perfil tarda”.
```

| Criterio | ¿Cumple? |
|----------|----------|
| Descubre `GetProfile` / `UserProfile` | No |
| Reutiliza `AuthApiClient` | No |
| Evidencia de paths | No |
| Sin sleeps | No |

**Score:** 2 · **Correcciones estimadas:** 4–5

---

## 3. Brazo B — Analyst → Planner

### Evidencia

| Path | Reason |
|------|--------|
| `Clients/AuthApiClient.cs` | `GetProfile(string accessToken)` |
| `Models/AuthModels.cs` | `UserProfile` DTO |
| `knowledge/framework/component-catalog.md` | Inventario post-refresh |
| `knowledge/known-issues/eval-traps.md` | KI-03 |
| `Hooks/AuthHooks.cs` | Fake API por escenario |
| `TokenRefreshSteps.cs` / `LoginSteps.cs` | Patrón steps + client |

### Analysis

```yaml
request_id: USER-PROFILE-GET
summary: >
  Automatizar GET de perfil autenticado. FakeAuthApi.GetProfile ya existe;
  no hay feature ni steps.
proposed_coverage:
  positive:
    - Token lab-token-* → UserProfile con Username/DisplayName/Role
  negative:
    - Token vacío → null / fallo explícito en step
    - Token sin prefijo lab-token- → null
  edge:
    - Token lab-token-refreshed (post-refresh) también es válido por prefijo
assumptions:
  - No hay HTTP real; FakeAuthApi
  - “No autorizado” se modela como null hoy (no exception)
open_questions:
  - ¿Exponer error code en GetProfile o mantener null + assert en step/validator?
  - ¿Encadenar Given login/refresh o fabricar access token como en refresh?
out_of_scope:
  - UI profile page
  - Actualizar perfil (PUT)
evidence:
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Clients/AuthApiClient.cs
    reason: GetProfile contract
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Models/AuthModels.cs
    reason: UserProfile shape
```

**Gate 1 (simulado):** APPROVED

### Plan

```yaml
request_id: USER-PROFILE-GET
reuse:
  builders: []
  validators: []  # no hay UserProfileValidator aún
  steps: []
  pages_or_clients:
    - AuthApiClient
    - FakeAuthApi
    - UserProfile model
create_only_if_needed:
  - UserProfileValidator — ShouldExist / ShouldMatch (justificado: no hay validator de perfil)
  - UserProfileSteps + Profile.feature
  - AccessTokenData (Support) — fabricar lab-token-valid_user; opcional Given I am authenticated via login
files_likely_affected:
  - src/AutomationLab/Validators/UserProfileValidator.cs
  - tests/.../Features/Profile.feature
  - tests/.../Steps/UserProfileSteps.cs
  - tests/.../Support/AccessTokenData.cs
  - knowledge/framework/component-catalog.md
risks:
  - id: R-NULL-VS-ERROR
    severity: medium
    note: null no distingue vacío vs inválido; documentar en validator
  - id: R-TOKEN-SOURCE
    severity: low
    note: Preferir fixture AccessTokenData alineado a FakeAuthApi, o Given login reusando LoginRequestBuilder
implementation_steps:
  - Añadir UserProfileValidator
  - Feature con @USER-PROFILE-GET (+ negativo)
  - Steps vía AuthApiClient.GetProfile
  - Actualizar catálogo
  - dotnet test
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
evidence:
  - path: knowledge/anti-patterns/anti-patterns.md
    reason: No inventar HTTP client paralelo
  - path: labs/.../Steps/TokenRefreshSteps.cs
    reason: Patrón Given fixture + client
```

**Gate 2 (simulado):** APPROVED  
**Score:** 9 · **Correcciones estimadas:** 0–1 (null vs error code)

---

## 4. Scorecard

| Criterio | Few-shot | Workflow |
|----------|----------|----------|
| Cita GetProfile existente | Fallo | OK |
| Reusa AuthApiClient | Fallo | OK |
| No servicio HTTP nuevo | Fallo | OK |
| Validator justificado | N/A (crea de más) | OK |
| Evidencia | Fallo | OK |

**Winner:** Workflow

### Implementación post Gate 2

- `UserProfileValidator`, `UserProfileSteps`, `AccessTokenData`, `Profile.feature`
- Reuso: `AuthApiClient.GetProfile` / `UserProfile`
- `dotnet test`: **10 passed** (suite completa lab)

---

## 5. Baseline update

Historias con eval few-shot vs workflow:  
1. AUTH-TOKEN-REFRESH (001)  
2. AUTH-DUPLICATE-BUILDER (001 trampa)  
3. USER-PROFILE-GET (002)  

→ **3/5+** hacia cierre Fase 0.
