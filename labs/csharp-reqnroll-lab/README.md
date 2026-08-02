# C# Reqnroll Lab

Gemelo reducido del stack laboral (**C# · Reqnroll · xUnit · Builders · Validators**) para la práctica de IA.

API Auth **in-memory** (`FakeAuthApi`) — sin red.

**Estado:** alineado al cierre de [Fase 0](../../docs/ai-evolution/PHASE-0-COMPLETE.md).

## Estructura

```text
labs/csharp-reqnroll-lab/
├── AutomationLab.slnx
├── src/AutomationLab/
│   ├── Builders/LoginRequestBuilder.cs
│   ├── Validators/LoginResponseValidator.cs
│   ├── Validators/UserProfileValidator.cs
│   ├── Clients/AuthApiClient.cs   # + FakeAuthApi
│   ├── Models/
│   └── Pages/LoginPage.cs
└── tests/AutomationLab.Tests/
    ├── Features/Login.feature
    ├── Features/TokenRefresh.feature
    ├── Features/Profile.feature
    ├── Steps/
    ├── Support/RefreshTokenData.cs
    ├── Support/AccessTokenData.cs
    └── Hooks/AuthHooks.cs
```

## Comandos

```bash
cd labs/csharp-reqnroll-lab
dotnet test
# Esperado: 10 passed
```

## Historias / tags

| Tag | Estado |
|-----|--------|
| `@AUTH-LOGIN-OK` / `@AUTH-LOGIN-NEG` / `@AUTH-LOCKOUT` | Automatizado |
| `@AUTH-TOKEN-REFRESH` | Automatizado |
| `@USER-PROFILE-GET` | Automatizado |

Catálogo: `knowledge/framework/component-catalog.md`.  
Evals: `docs/ai-evolution/evals/`.

## Cómo usarlo con IA

1. **automation-analyst** → Gate 1.
2. **automation-planner** (catálogo + anti-patrones) → Gate 2.
3. Implementar solo con plan aprobado; actualizar catálogo.
4. Trampas: AUTH-DUPLICATE-BUILDER; pedir login negativo “nuevo” (ya cubierto).
