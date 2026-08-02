# Skeleton — árbol mínimo A0–A3

Plantilla de directorios. Sustituir `<TARGET_>` y nombres de dominio.

```text
docs/ai-evolution/
├── README.md
├── 00-vision-and-baseline.md
├── 01-use-cases.md
├── 02-risks.md
├── workflow-analyst-planner.md
├── PORTABLE-BLUEPRINT.md          # copiar o enlazar desde el lab
├── LLM-PORTABILITY.md             # opcional A0
├── NEXT-STEPS.md
└── evals/
    ├── README.md
    ├── RUBRIC.md
    ├── 001-<STORY-NEW>.md
    ├── 002-<STORY-COVERED>.md
    └── 003-<STORY-DUP-TRAP>.md

prompts/
├── contracts/
│   ├── README.md
│   ├── analysis.v1.yaml
│   └── plan.v1.yaml
├── fragments/
│   ├── guardrails.md
│   ├── anti-patterns.md
│   ├── gate-criteria.md
│   └── context-load-order.md
└── examples/
    └── approved/
        ├── 01-<story>-analysis.md
        ├── 02-<already-covered>-plan.md
        └── 03-<duplicate>-reject.md

knowledge/
├── README.md
├── agents/
│   ├── contracts.md
│   └── handoffs.md
├── framework/
│   └── component-catalog.md
├── patterns/
│   └── approved-patterns.md
├── anti-patterns/
│   └── anti-patterns.md
├── coding-standards/
│   └── naming.md
├── review-checklists/
│   └── guardrails.md
├── examples/
│   └── README.md
├── decisions/
│   ├── ADR-001-platform-vs-subject.md
│   └── ADR-002-orchestration.md
└── known-issues/
    └── eval-traps.md

# Surface — elegir según IDE del destino
.github/agents/
├── automation-analyst.agent.md
├── automation-planner.agent.md
├── automation-builder.agent.md      # stub OK en A3
└── automation-reviewer.agent.md     # stub OK en A3
.github/prompts/
├── automation-analyst.prompt.md
├── automation-planner.prompt.md
├── automation-builder.prompt.md
└── automation-reviewer.prompt.md

.cursor/rules/
└── ai-evolution.mdc                 # si usan Cursor
```

## A4+ (no crear en la primera inserción salvo pedido)

```text
tools/registry/v1/
├── registry.json
├── PERMISSIONS.md
└── README.md
tools/workflow/v1/
tools/patches/v1/
├── allowlist.json
├── recipes.json
└── recipes/
scripts/
├── tools_runner.py
├── workflow_runner.py
├── patch_pipeline.py
├── review_diff.py
└── run_all_smokes.sh
```

## Campos `plan.v1.reuse` — renombrar al destino

| Lab (referencia) | Destino ejemplo |
|------------------|-----------------|
| `builders` | `builders` / `factories` / `fixtures` |
| `validators` | `validators` / `assertions` |
| `steps` | `steps` / `step_definitions` |
| `pages_or_clients` | `pages` / `api_clients` / `screens` |
