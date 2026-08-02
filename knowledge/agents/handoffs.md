# Handoffs — Analyst → Planner → Builder → Reviewer

```text
Request
  → Analyst (analysis.v1 + evidence)
  → Gate 1 human
  → Planner (plan.v1 + reuse)
  → Gate 2 human
  → Builder (propose_patch / recipe)     [skip if already_covered]
  → Reviewer (review_diff on proposal.diff)
  → Gate 3 human
  → patch_pipeline apply --gate3-approved [--run-tests]
  → STOP (no merge by agents)
```

## Artifact checklist per handoff

### Analyst → Gate 1

- [ ] YAML matches `prompts/contracts/analysis.v1.yaml`
- [ ] `evidence.length >= 1`
- [ ] Assumptions ≠ invented facts

### Planner → Gate 2

- [ ] `policy_checks.searched_before_create: true` if creating
- [ ] `create_only_if_needed` justified or empty
- [ ] Tool hits cited

### Builder → Reviewer

- [ ] `proposal_id` exists under `.forgeone/runs/patches/`
- [ ] Paths allowlisted
- [ ] No apply attempted

### Reviewer → Gate 3

- [ ] Findings mapped to taxonomy codes
- [ ] High severity → recommend reject
- [ ] No patch authored by Reviewer
