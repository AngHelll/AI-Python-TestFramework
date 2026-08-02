---
agent: automation-reviewer
---

# Review automation diff

**Fixture (optional):** ${input:fixture}
**Path (optional):** ${input:path}

## Required behavior

1. Run read-only review:
   - `python3 scripts/tools_runner.py invoke review_diff --arg fixture=<uc05|uc06|uc07> --json`
   - or `--arg path=knowledge/examples/review/...`
2. Present findings with code, severity, path, line, message.
3. Reference `knowledge/examples/review/taxonomy.md`.
4. Do not propose a patch unless the user explicitly asks after acknowledging findings.
