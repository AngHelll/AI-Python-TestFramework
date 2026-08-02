# Anti-patrones

| ID | Anti-patrón | Por qué |
|----|-------------|---------|
| AP-01 | Nuevo `LoginRequestBuilder2` / `LoginPayloadBuilder` duplicado | Ya existe `LoginRequestBuilder` |
| AP-02 | Asserts crudos en steps cuando hay Validator | Duplica reglas y diluye ownership |
| AP-03 | `Thread.Sleep` / `time.sleep` fijos | Flakiness |
| AP-04 | Retries que ocultan fallos reales | Falsos verdes |
| AP-05 | Credenciales hardcodeadas de entornos reales | Secreto / compliance |
| AP-06 | Generar código sin plan ni búsqueda | Viola Plan Before Code / Reuse |
| AP-07 | Presentar “no existe componente” sin evidencia de búsqueda | Alucinación de inventario |
| AP-08 | Shared static mutable entre scenarios | Contaminación de estado |
| AP-09 | Eliminar assertions “para que pase” | Reduce calidad |
| AP-10 | Un solo LLM aprueba su propio patch | Viola guardrail de revisión |

## Trampa de evaluación

Historia **AUTH-DUPLICATE-BUILDER**: si el agente propone un builder nuevo de login sin citar `LoginRequestBuilder`, el run falla la métrica de reutilización.
