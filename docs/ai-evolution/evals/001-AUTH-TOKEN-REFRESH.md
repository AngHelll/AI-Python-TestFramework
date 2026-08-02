# Eval run 001 — AUTH-TOKEN-REFRESH (+ trampa builder)

**Fecha:** 2026-07-30  
**Target:** `labs/csharp-reqnroll-lab`  
**Request ID:** `AUTH-TOKEN-REFRESH`  
**Dominio:** Auth  
**Constraints:** solo API; no modificar código en esta eval (plan only)

## 1. Entrada común

> Como usuario autenticado quiero refrescar el access token con un refresh token válido para continuar la sesión sin re-login.  
> Aceptación: refresh válido → nuevo access token; inválido/vacío → error claro.  
> Preferir reutilizar el framework existente.

## 2. Brazo A — Few-shot ingenuo (sin retrieval ni gates)

Simula el uso actual: prompt corto + un ejemplo de login, sin obligar búsqueda en repo.

### Salida típica observada / esperada (síntesis de fallo)

```text
Crear TokenRefreshRequestBuilder y TokenRefreshResponseValidator.
Agregar AuthTokenService nuevo.
Escribir feature TokenRefresh.feature desde cero.
Steps con asserts FluentAssertions inline.
Opcional: Thread.Sleep(500) tras refresh "por estabilidad".
```

### Defectos vs golden / catálogo

| Criterio | ¿Cumple? | Nota |
|----------|----------|------|
| Descubre `FakeAuthApi.RefreshToken` | No | Propone servicio nuevo |
| Reutiliza `AuthApiClient` | No | — |
| No duplica login builder | N/A / riesgo | Inventa builder paralelo |
| Feature ya existe (`@ignore`) | No | Propone crear de cero |
| Evidencia de paths | No | — |
| Sin sleeps | No | Sugiere sleep |
| Separación análisis/plan | No | Salta a código |

**Score brazo A (0–10):** 2  
**Correcciones humanas estimadas:** 4–6 (reuso, feature existente, anti-sleep, quitar builders duplicados)

---

## 3. Brazo B — Analyst → Planner (workflow v0.1)

### 3.1 Context recovery (evidencia)

| Path | Reason |
|------|--------|
| `knowledge/framework/component-catalog.md` | Inventario builders/validators/clients |
| `knowledge/examples/AUTH-TOKEN-REFRESH-golden.md` | Golden humano |
| `knowledge/known-issues/eval-traps.md` | KI-01 feature @ignore |
| `knowledge/anti-patterns/anti-patterns.md` | AP-01, AP-02, AP-03 |
| `labs/.../Clients/AuthApiClient.cs` | Contrato `RefreshToken` / `INVALID_REFRESH` |
| `labs/.../Features/TokenRefresh.feature` | Escenario ya escrito, `@ignore` |
| `labs/.../Features/Login.feature` | Patrón de tags/steps |
| `labs/.../Steps/LoginSteps.cs` | Patrón Builder + Validator + Page/Client |
| `labs/.../Validators/LoginResponseValidator.cs` | Reuso posible (`ShouldBeSuccessful`) |
| `labs/.../Builders/LoginRequestBuilder.cs` | Confirmar que NO aplica a refresh token string |
| `labs/.../Hooks/AuthHooks.cs` | Fake API por escenario |

### 3.2 Analysis (Analyst)

```yaml
request_id: AUTH-TOKEN-REFRESH
summary: >
  Automatizar refresh de access token vía API Auth del lab.
  Ya existe superficie FakeAuthApi.RefreshToken y un feature @ignore
  sin step bindings.
proposed_coverage:
  positive:
    - Refresh con token "lab-refresh-*" retorna Success y AccessToken no vacío
  negative:
    - Refresh token vacío → ErrorCode INVALID_REFRESH
    - Refresh token sin prefijo lab-refresh- → INVALID_REFRESH
  edge:
    - Distinguir access token (lab-token-*) vs refresh token (lab-refresh-*)
assumptions:
    - Solo API in-memory; sin UI
    - LoginResponse es el DTO de salida del refresh (contrato actual)
open_questions:
    - ¿Se requiere escenario Outline con varios refresh tokens inválidos o basta un negativo?
    - ¿Se emite refresh token en Login hoy? (Login solo devuelve AccessToken)
out_of_scope:
    - GetProfile / USER-PROFILE-GET
    - Integración Jira/XRay real
    - Parches de código en esta fase
evidence:
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Clients/AuthApiClient.cs
    reason: Contrato RefreshToken y códigos de error
  - path: labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/TokenRefresh.feature
    reason: Feature planned ya presente
  - path: knowledge/examples/AUTH-TOKEN-REFRESH-golden.md
    reason: Expectativa humana de cobertura
```

**Gate 1 (simulado — humano):** APPROVED  
Motivo: cobertura +/-/edge alineada al contrato; supuestos y dudas explícitas; no inventa keys.

### 3.3 Plan (Planner)

```yaml
request_id: AUTH-TOKEN-REFRESH
reuse:
  builders: []   # LoginRequestBuilder no aplica (payload es string refresh)
  validators:
    - LoginResponseValidator.ShouldBeSuccessful  # camino feliz
    - LoginResponseValidator.ShouldFailWith      # INVALID_REFRESH
  steps: []  # no hay steps de refresh aún; reutilizar patrón LoginSteps
  pages_or_clients:
    - AuthApiClient
    - FakeAuthApi
    - IAuthApi via ScenarioContext (AuthHooks)
create_only_if_needed:
  - TokenRefreshSteps — bindings Given/When/Then del feature existente
  - (opcional) helper de test data AsValidRefreshToken en Support/ — solo si evita magic strings repetidos; NO un RequestBuilder duplicado de login
files_likely_affected:
  - labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Steps/TokenRefreshSteps.cs  # nuevo
  - labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/TokenRefresh.feature  # quitar @ignore; añadir escenario negativo
  - labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Support/RefreshTokenData.cs  # opcional
risks:
  - id: R-TOKEN-CONFUSION
    severity: medium
    note: Mezclar lab-token-* con lab-refresh-* en Given
  - id: R-LOGIN-DTO
    severity: low
    note: Refresh reutiliza LoginResponse; documentar para no crear DTO gemelo sin necesidad
  - id: R-NO-REFRESH-FROM-LOGIN
    severity: medium
    note: Login no emite refresh token; el Given debe fabricar lab-refresh-demo (fake), no encadenar Login
implementation_steps:
  - Confirmar contrato RefreshToken en FakeAuthApi
  - Añadir TokenRefreshSteps usando AuthApiClient del ScenarioContext
  - Reusar LoginResponseValidator en Then
  - Extender feature con escenario negativo INVALID_REFRESH
  - Quitar @ignore
  - dotnet test; filtrar @AUTH-TOKEN-REFRESH
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
evidence:
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Validators/LoginResponseValidator.cs
    reason: Reuso de asserts de LoginResponse
  - path: labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Hooks/AuthHooks.cs
    reason: Inyección FakeAuthApi
  - path: knowledge/anti-patterns/anti-patterns.md
    reason: Evitar AP-01/AP-03
```

**Gate 2 (simulado — humano):** APPROVED  
Motivo: reutilización explícita; create justificado; sin segundo login builder; riesgos útiles.

**Score brazo B (0–10):** 9  
**Correcciones humanas estimadas:** 0–1 (decidir Outline vs un solo negativo)

---

## 4. Scorecard vs golden

| Criterio golden | Few-shot | Workflow |
|-----------------|----------|----------|
| Menciona FakeAuthApi / AuthApiClient.RefreshToken | Fallo | OK |
| Feature existente / no recrear de cero | Fallo | OK |
| No crear Login builder nuevo | Fallo / riesgo | OK |
| Reusar o extender validator de LoginResponse | Fallo | OK |
| Riesgo access vs refresh | Fallo | OK |
| Evidencia de paths | Fallo | OK |
| Sin patch en esta fase | N/A (quería código) | OK |

**Winner:** Workflow Analyst→Planner

### Implementación post Gate 2 (misma fecha)

Ejecutada bajo supervisión humana (“Adelante”):

- `TokenRefreshSteps`, `RefreshTokenData`
- Feature sin `@ignore` + 2 negativos `INVALID_REFRESH`
- `dotnet test`: **6 passed** (3 login + 3 refresh)

---

## 5. Trampa AUTH-DUPLICATE-BUILDER (mini)

**Prompt trampa:** “Necesito un builder nuevo para armar el payload de login en Auth.”

| Enfoque | Resultado esperado |
|---------|-------------------|
| Few-shot | Propone `AuthLoginPayloadBuilder` / similar |
| Planner con catálogo | Cita `LoginRequestBuilder`; `create_only_if_needed: []` |

**Resultado esta sesión (Planner):** reutilizar `LoginRequestBuilder` (`AsValidUser` / `WithUsername`…). **PASS**

---

## 6. Línea base registrada

| Métrica | Few-shot (A) | Workflow (B) |
|---------|--------------|--------------|
| Score calidad plan (0–10) | 2 | 9 |
| Componentes reutilizados citados | 0 | 4+ |
| Omisiones críticas | 3+ | 0 |
| Correcciones humanas estimadas | 4–6 | 0–1 |
| ¿Generó patch no pedido? | Sí (implícito) | No |
| Gate 1 / Gate 2 | N/A | Approved / Approved |

Historias cubiertas en run 001: `AUTH-TOKEN-REFRESH`, `AUTH-DUPLICATE-BUILDER` (trampa).

Pendiente para ampliar baseline: `AUTH-LOGIN-OK` (sanity), `USER-PROFILE-GET`, `AUTH-LOGIN-NEG` como análisis de extensión.
