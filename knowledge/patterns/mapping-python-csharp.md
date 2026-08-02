# Mapeo de patrones Python ↔ C# (lab)

Usar esta tabla para transferir propuestas entre el framework Python y `labs/csharp-reqnroll-lab/`.

| Concepto | Python | C# lab |
|----------|--------|--------|
| BDD runner | Behave | Reqnroll |
| Unit / technical tests | Pytest | xUnit (vía Reqnroll.xUnit) |
| Feature files | `features/*.feature` | `tests/.../Features/*.feature` |
| Step defs | `features/steps/` | `tests/.../Steps/` |
| Hooks | `features/environment.py` | `Hooks/` + `[BeforeScenario]` |
| Page Object | `pages/*_page.py` + `BasePage` | `Pages/` (facade delgada) |
| Request construction | helpers / dicts | `Builders/*Builder` |
| Assertions de respuesta | asserts en steps | `Validators/*Validator` |
| API client | (añadir si aplica) | `Clients/AuthApiClient` + `IAuthApi` |
| Config | `.env` / `config/settings.py` | (lab: in-memory; prod: IOptions) |
| Test data | `test_data/*.json` | Builders (`AsValidUser`) |
| Logging | `utils/logger.py` | (añadir ILogger en iteraciones) |
| AI context | `prompts/context/` | `knowledge/` + este mapeo |

## Reglas de reutilización (ambos stacks)

1. Buscar Builder/Validator/Step existente antes de crear.
2. Steps orquestan; no embuten lógica de negocio larga.
3. Validators concentran assertions de respuesta.
4. Builders concentran datos de request deterministas.
5. No `Thread.Sleep` / `time.sleep` en caminos felices.

## Componentes canónicos del lab C# (no duplicar)

- `LoginRequestBuilder`
- `LoginResponseValidator`
- `AuthApiClient` / `FakeAuthApi`
- `LoginPage`
- Steps en `LoginSteps`
