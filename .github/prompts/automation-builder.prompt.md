---
agent: automation-builder
---

# Propose controlled patch

**Recipe:** ${input:recipe}
**Workflow run id (optional):** ${input:run_id}

## Required behavior

1. Confirm Gate 2 approved plan exists (run id or user statement).
2. If plan `already_covered` → stop; do not propose.
3. Run:
   `python3 scripts/patch_pipeline.py propose --recipe ${input:recipe} [--from-run ${input:run_id}] --json`
4. Return `proposal_id`, `status`, review codes, paths.
5. Do **not** apply. Tell user to run Reviewer then Gate 3 apply if clean.
