# Knowledge Base v0

Base de conocimiento para la práctica de IA.

**Alineado a:** [Fase 0 cerrada](../docs/ai-evolution/PHASE-0-COMPLETE.md) (2026-07-30).

Complementa `prompts/context/` (referencia técnica del framework Python) con conocimiento **gobernado** orientado a workflows Analyst → Planner → Reviewer.

## Estructura

```text
knowledge/
├── architecture/       # Capas y límites
├── framework/          # Inventario de componentes reutilizables
├── patterns/           # Patrones aprobados
├── anti-patterns/      # Qué no generar
├── bdd/                # Convenciones Behave / Reqnroll
├── api/                # Contratos / clientes
├── xray/               # Tags y mapeo (sintético en lab)
├── coding-standards/   # Naming y estilo
├── examples/           # Golden analyses / plans
├── known-issues/       # Deuda y trampas de eval
├── decisions/          # ADRs
└── review-checklists/  # Guardrails y checklists
```

## Targets

| Target | Path | Stack |
|--------|------|-------|
| Python framework | repo root | Pytest, Behave, POM |
| C# lab | `labs/csharp-reqnroll-lab/` | Reqnroll, xUnit, Builders, Validators |

Ver `patterns/mapping-python-csharp.md` antes de proponer código en el target incorrecto.

## Ownership

- Cambios en `knowledge/` deben ir con el cambio de código o ADR correspondiente.
- Ejemplos canónicos solo tras Gate humano (no auto-promover salidas de LLM).
