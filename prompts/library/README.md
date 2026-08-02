# Prompt Library v1

Formal prompt inventory for the AI evolution practice (Phase 1).

## By purpose

| Purpose | Surface | Contract / fragment | Notes |
|---------|---------|---------------------|-------|
| Functional analysis | `.github/prompts/automation-analyst.prompt.md` + agent | `contracts/analysis.v1.yaml` | Gate 1 |
| Technical plan | `.github/prompts/automation-planner.prompt.md` + agent | `contracts/plan.v1.yaml` | Gate 2 |
| Controlled patch propose | `.github/prompts/automation-builder.prompt.md` | Phase 7 recipes | Gate 3 later |
| Diff review | `.github/prompts/automation-reviewer.prompt.md` | review taxonomy | Observe only |
| Shared constraints | `fragments/*` | — | Include in both |
| Role limits | `knowledge/agents/contracts.md` | — | Phase 8 |
| Framework how-to (Python) | `prompts/context/*` | — | Legacy AI context |
| POM / BDD / pytest | `.github/prompts/pom-author|bdd-behave|pytest-debugger` | — | Post Gate 2 / debug |

## Approved few-shots (human-curated)

| ID | File | Teaches |
|----|------|---------|
| FS-01 | `examples/approved/01-token-refresh-analysis.md` | Discover existing API + @ignore feature |
| FS-02 | `examples/approved/02-already-covered-plan.md` | Empty create list when covered |
| FS-03 | `examples/approved/03-duplicate-builder-reject.md` | Reuse LoginRequestBuilder |

Do **not** promote raw LLM outputs into this folder without Gate review.

## Anti-patterns for prompts themselves

- Mixing analysis + full code in one prompt response
- Omitting `evidence`
- Softening severity of Sleep / secrets
- Unversioned output shapes (always cite `analysis.v1` / `plan.v1`)
