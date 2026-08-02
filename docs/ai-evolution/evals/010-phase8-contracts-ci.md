# Eval 010 — Agent contracts + CI smokes

**Fecha:** 2026-07-30  
**Phase:** 8

## Checks

| Check | How | Result |
|-------|-----|--------|
| Contracts exist | `knowledge/agents/contracts.md` | Present |
| Handoffs exist | `knowledge/agents/handoffs.md` | Present |
| Builder agent | `.github/agents/automation-builder.agent.md` | Present |
| Local smokes script | `bash scripts/run_all_smokes.sh` | Run locally / CI |
| CI workflow | `.github/workflows/ai-evolution-smokes.yml` | Added |

Reproduce:

```bash
bash scripts/run_all_smokes.sh
```

Docs: [PHASE-8.md](../PHASE-8.md)
