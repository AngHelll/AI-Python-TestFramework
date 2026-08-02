# Riesgos iniciales (Fase 0)

| ID | Riesgo | Impacto | Mitigación |
|----|--------|---------|------------|
| R-01 | Sobreautomatizar antes de knowledge/evals | Alto | Seguir secuencia del roadmap; Fase 5 sin write |
| R-02 | Aprender solo en Python y no transferir a C# | Alto | Lab `csharp-reqnroll-lab` + mapeo de patrones |
| R-03 | Contexto desactualizado | Medio | Ownership de `knowledge/`; ejemplos canónicos versionados |
| R-04 | Confianza excesiva en LLM | Alto | Human gates; reglas deterministas; evidencia obligatoria |
| R-05 | Falsos positivos del Reviewer | Medio | Taxonomía + medición FP antes de integrar PR |
| R-06 | Vendor lock-in (un solo SDK/modelo) | Medio | Contratos de tools/prompts independientes del vendor |
| R-07 | Acceso excesivo (shell, secretos) | Alto | Tools read-only primero; allowlist de rutas |
| R-08 | Complejidad prematura (LangGraph/MCP) | Medio | Adoptar solo con criterios del §15 del roadmap |
| R-09 | Métricas solo de velocidad | Medio | Incluir duplicación, rechazo, flakiness, correcciones |
| R-10 | Filtrar secretos / datos reales de trabajo | Alto | Lab sintético; nunca copiar `.env` laboral |

## Acciones que la IA nunca hace sin aprobación humana

1. Merge / push a main.
2. Cambiar dependencias o paquetes globales.
3. Modificar secretos o CI secrets.
4. Eliminar pruebas o reducir assertions.
5. Ejecutar comandos arbitrarios fuera de la tool registry.
6. Aprobar su propio cambio como única revisión.
