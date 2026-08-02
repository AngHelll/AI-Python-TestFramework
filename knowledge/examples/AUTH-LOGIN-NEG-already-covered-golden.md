# Ejemplo canónico — AUTH-LOGIN-NEG (already covered)

## Estado

Cobertura **preexistente** en `Login.feature` (`@AUTH-LOGIN-NEG`).  
Eval 003: el resultado correcto del workflow es **no crear** automatización nueva.

## Análisis (resumen)

- Pedido de login inválido + mensaje de error.
- Ya cubierto con `LoginRequestBuilder.AsInvalidUser` + `LoginResponseValidator.ShouldFailWith`.

## Plan de referencia

- `create_only_if_needed: []`
- Riesgo alto: duplicar feature/steps.
- Acción: marcar ticket Already Covered / solo tags si aplica.
