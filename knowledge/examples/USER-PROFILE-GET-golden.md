# Ejemplo canónico — USER-PROFILE-GET

## Estado

**Implementado** tras Gate 2 (eval 002) — 2026-07-30.  
Feature: `labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/Profile.feature`.

## Análisis (resumen)

- `AuthApiClient.GetProfile` / `UserProfile` ya existían.
- Unauthorized = `null` (sin error code).
- Cobertura: token válido, token de refresh, inválido, vacío.

## Plan ejecutado

- **Reutilizado:** `AuthApiClient`, `FakeAuthApi`, modelo `UserProfile`.
- **Creado:** `UserProfileValidator`, `UserProfileSteps`, `AccessTokenData`, `Profile.feature`.
- **No creado:** HttpClient paralelo ni builder de login duplicado.
