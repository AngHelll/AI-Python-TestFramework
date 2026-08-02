# FS-02 — Already covered plan (approved)

**Source golden:** `knowledge/examples/AUTH-LOGIN-NEG-already-covered-golden.md`  
**Eval:** `docs/ai-evolution/evals/003-AUTH-LOGIN-NEG-coverage.md`  
**Contract:** `plan.v1`

## User (abbreviated)

Need automation for invalid login + error message.

## Assistant (plan excerpt — approved shape)

```yaml
request_id: AUTH-LOGIN-NEG
reuse:
  builders: [LoginRequestBuilder]
  validators: [LoginResponseValidator]
  steps: [LoginSteps]
  pages_or_clients: [LoginPage, AuthApiClient]
create_only_if_needed: []
files_likely_affected: []
risks:
  - id: R-DUPLICATE-FEATURE
    severity: high
    note: Creating LoginNegative.feature would duplicate @AUTH-LOGIN-NEG
implementation_steps:
  - Confirm existing scenario with dotnet test
  - Mark request Already Covered (optional tag only)
evidence:
  - path: labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/Login.feature
    reason: @AUTH-LOGIN-NEG scenario already present
policy_checks:
  searched_before_create: true
  no_critical_files_without_flag: true
meta:
  contract: plan.v1
  already_covered: true
```

## Why this is approved

Empty create list is a valid plan; duplication called out as high risk.
