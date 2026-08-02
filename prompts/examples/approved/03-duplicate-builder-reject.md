# FS-03 — Duplicate builder reject (approved)

**Trap:** AUTH-DUPLICATE-BUILDER  
**Eval:** `docs/ai-evolution/evals/001-AUTH-TOKEN-REFRESH.md` §5  
**Contract:** `plan.v1` (fragment)

## User (trap)

I need a new builder to assemble the Auth login payload.

## Assistant (approved response pattern)

```yaml
request_id: AUTH-DUPLICATE-BUILDER
reuse:
  builders: [LoginRequestBuilder]
  validators: []
  steps: []
  pages_or_clients: []
create_only_if_needed: []
files_likely_affected: []
risks:
  - id: R-AP-01
    severity: high
    note: A second login builder violates AP-01 / catalog
implementation_steps:
  - Use LoginRequestBuilder.AsValidUser / WithUsername / WithPassword
evidence:
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Builders/LoginRequestBuilder.cs
    reason: Canonical login request builder
  - path: knowledge/framework/component-catalog.md
    reason: Inventory
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
meta:
  already_covered: true
  contract: plan.v1
```

## Fail pattern (never promote)

Proposing `AuthLoginPayloadBuilder` / `LoginRequestBuilder2` without citing the existing type.
