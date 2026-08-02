# Agent contracts v1 — specialized roles

**Phase:** 8  
**Status:** Active  
**Principle:** One role per stage. No agent approves its own change as sole review.

| Agent | Produces | Must not | Handoff to |
|-------|----------|----------|------------|
| **Analyst** | `analysis.v1` | Code, patches, plans | Human Gate 1 → Planner |
| **Planner** | `plan.v1` | Patches, merge | Human Gate 2 → Builder (optional) |
| **Builder** | Patch **proposal** via recipes/`propose_patch` | Apply without Gate 3, merge | Reviewer → Gate 3 |
| **Reviewer** | Findings (taxonomy codes) | Auto-fix, approve alone | Human Gate 3 / stop |
| **Stability Reviewer** | `STAB-*` only | Other categories as primary | Gate 3 |
| **XRay Reviewer** | `XRAY-*` only | Inventing corp keys | Gate 3 |
| **Security Reviewer** | `SEC-*` only | Exfiltrating secrets | Gate 3 |

## Surfaces

| Agent | Copilot agent | Prompt | Primary tools |
|-------|---------------|--------|---------------|
| Analyst | `automation-analyst` | `automation-analyst.prompt.md` | `find_*`, `find_knowledge`, `workflow_runner` |
| Planner | `automation-planner` | `automation-planner.prompt.md` | `find_*`, `validate_naming`, `detect_forbidden_patterns` |
| Builder | `automation-builder` | `automation-builder.prompt.md` | `propose_patch` only (no apply) |
| Reviewer | `automation-reviewer` | `automation-reviewer.prompt.md` | `review_diff` |

## Escalation to human

| Situation | Action |
|-----------|--------|
| Missing evidence / empty tool hits | Gate reject → Analyst |
| `already_covered: true` | Stop; no Builder |
| Review `severity=high` | Block Gate 3; no apply |
| Ambiguous domain / secrets | Stop; human owns decision |
| Recipe missing for request | Human writes recipe or defers LLM body |

## Traceability

Every handoff should reference:

- `request_id`
- `run_id` (workflow) and/or `proposal_id` (patch)
- `tools_invoked` / review `codes`
- Gate decision + note
