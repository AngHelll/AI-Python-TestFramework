# BDD — convenciones lab

## Tags de historia (sintéticos tipo XRay)

| Tag | Historia |
|-----|----------|
| `@AUTH-LOGIN-OK` | Login exitoso |
| `@AUTH-LOGIN-NEG` | Credenciales inválidas |
| `@AUTH-LOCKOUT` | Lockout |
| `@AUTH-TOKEN-REFRESH` | Refresh (planned) |
| `@smoke` | Suite rápida |
| `@ignore` | Excluido de ejecución |

## Estilo Gherkin

- Escenarios en inglés (lab); el framework laboral puede usar ES — documentar en knowledge cuando se añada.
- Un escenario = una intención verificable.
- Evitar steps que mezclen Given+When+Then.

## Steps

- Reutilizar steps existentes por frase exacta antes de crear sinónimos.
