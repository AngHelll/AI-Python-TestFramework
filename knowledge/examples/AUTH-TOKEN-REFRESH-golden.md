# Ejemplo canónico — AUTH-TOKEN-REFRESH (humano de referencia)

## Estado

**Implementado** tras Gate 2 (eval 001) — 2026-07-30.  
Ver `labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/TokenRefresh.feature`.

## Análisis (resumen)

- Necesidad: refrescar access token con refresh token válido.
- Cobertura positiva: refresh OK → nuevo access token.
- Negativos: refresh vacío/inválido → `INVALID_REFRESH`.
- Existe API: `FakeAuthApi.RefreshToken` / `AuthApiClient.RefreshToken`.

## Plan ejecutado

- **Reutilizado:** `AuthApiClient`, `FakeAuthApi`, `LoginResponseValidator`.
- **Creado:** `TokenRefreshSteps`, `RefreshTokenData` (fixtures, no login builder).
- **No creado:** nuevo Login builder ni validator gemelo.
- Escenarios: válido + inválido + vacío; `@ignore` eliminado.
