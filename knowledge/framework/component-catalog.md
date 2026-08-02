# Inventario de componentes reutilizables — C# lab

Target: `labs/csharp-reqnroll-lab/`  
Actualizado: 2026-07-30 (post Profile)

## Builders

| Tipo | Path | Dominio |
|------|------|---------|
| `LoginRequestBuilder` | `src/AutomationLab/Builders/LoginRequestBuilder.cs` | Auth login |

## Support / test data

| Tipo | Path | Dominio |
|------|------|---------|
| `RefreshTokenData` | `tests/.../Support/RefreshTokenData.cs` | Refresh fixtures |
| `AccessTokenData` | `tests/.../Support/AccessTokenData.cs` | Access token fixtures |

## Validators

| Tipo | Path | Dominio |
|------|------|---------|
| `LoginResponseValidator` | `src/AutomationLab/Validators/LoginResponseValidator.cs` | Login + refresh response |
| `UserProfileValidator` | `src/AutomationLab/Validators/UserProfileValidator.cs` | Profile presence/shape |

## Clients / Fakes

| Tipo | Path | Notas |
|------|------|-------|
| `IAuthApi` / `FakeAuthApi` | `Clients/AuthApiClient.cs` | `Login`, `RefreshToken`, `GetProfile` |
| `AuthApiClient` | idem | Facade |

## Pages

| Tipo | Path |
|------|------|
| `LoginPage` | `Pages/LoginPage.cs` |

## Features / Steps

| Feature | Tags | Steps |
|---------|------|-------|
| `Login.feature` | `@AUTH-LOGIN-OK`, `@AUTH-LOGIN-NEG`, `@AUTH-LOCKOUT` | `LoginSteps` |
| `TokenRefresh.feature` | `@AUTH-TOKEN-REFRESH` | `TokenRefreshSteps` |
| `Profile.feature` | `@USER-PROFILE-GET` | `UserProfileSteps` |

## Python espejo (referencia)

| Área | Path |
|------|------|
| Login feature | `features/login.feature` |
| Login steps | `features/steps/login_steps.py` |
| Login page | `pages/login_page.py` |
