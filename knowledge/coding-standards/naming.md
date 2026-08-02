# Naming (lab + transfer)

## C#

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Builder | `{Entity}{Purpose}Builder` | `LoginRequestBuilder` |
| Validator | `{Entity}{Purpose}Validator` | `LoginResponseValidator` |
| Feature file | PascalCase | `Login.feature` |
| Step class | `{Area}Steps` | `LoginSteps` |
| Tags historia | `@AUTH-...` | `@AUTH-LOGIN-OK` |

## Python

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Page | `*_page.py` / `*Page` | `login_page.py` |
| Test | `test_*.py` | `test_login.py` |
| Feature | snake or domain | `login.feature` |

No crear sinónimos (`LoginPayloadBuilder`) si ya existe el canónico.
