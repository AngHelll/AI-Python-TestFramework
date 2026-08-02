# Patrones aprobados

## Reuse Before Create

Antes de crear Builder, Validator, Step, Page o Helper:

1. Buscar por dominio (`Auth`, `User`, …).
2. Buscar por nombre (`LoginRequest*`, `*Validator`).
3. Documentar evidencia en el plan.
4. Solo entonces proponer `create_only_if_needed` con justificación.

## Builder

- Fluent API (`WithX` / `AsValidUser`).
- `Build()` retorna modelo inmutable o DTO.
- Sin I/O ni assertions.

## Validator

- Métodos estáticos o instancia sin estado compartido mutable entre tests.
- Un método = una intención (`ShouldBeSuccessful`, `ShouldFailWith`).
- Lanza o falla de forma explícita; no retorna `bool` silencioso para asserts críticos.

## Steps (BDD)

- Given/When/Then delgados.
- Delegan en Page/Client + Builder + Validator.
- Tags de escenario alineados a historias (`@AUTH-LOGIN-OK`).

## Fake / stub de laboratorio

- APIs in-memory (`FakeAuthApi`) para determinismo y evals.
- Estado fresco por escenario (hooks).
