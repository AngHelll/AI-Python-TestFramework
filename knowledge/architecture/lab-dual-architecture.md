# Arquitectura del laboratorio dual

```text
┌─────────────────────────────────────────────────────────────┐
│ Experiencias: Cursor · Copilot · Chat · (futuro CLI/MCP)    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ docs/ai-evolution + .github/agents + prompts + knowledge    │
│ Workflow Analyst → Planner → (Reviewer) + human gates       │
└───────────────────────────┬─────────────────────────────────┘
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌─────────────────────────┐   ┌───────────────────────────────┐
│ Python framework (root) │   │ labs/csharp-reqnroll-lab      │
│ Behave · Pytest · POM   │   │ Reqnroll · xUnit · Builders   │
└─────────────────────────┘   └───────────────────────────────┘
```

## Límites

- La plataforma IA **no** escribe al lab sin Gate 2 + (más adelante) Gate 3.
- El lab C# **no** es el monorepo laboral; es un gemelo reducido.
- Secretos reales nunca viven en este repo.
