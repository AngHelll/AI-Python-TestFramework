# Fragment — human gate criteria

## Gate 1 — Analysis

Approve when:

- Coverage (+/−/edge) is reasonable **or** `already_covered: true` with evidence
- Assumptions and open questions are explicit
- No invented Jira/XRay keys
- Evidence includes real paths

Reject when:

- Requirements invented as facts
- No evidence after claiming to search
- Code/patches included

## Gate 2 — Plan

Approve when:

- `searched_before_create: true` if anything is created
- Each `create_only_if_needed` entry is justified
- Risks are credible (include stability risks for UI)
- File paths are concrete
- No Sleep / secret / duplicate-builder proposals

Reject when:

- New Builder/Validator without catalog search
- Vague "update Auth area" instead of paths
- Patch diff presented as the plan
