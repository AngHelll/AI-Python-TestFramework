# FS-01 — Token refresh analysis (approved)

**Source golden:** `knowledge/examples/AUTH-TOKEN-REFRESH-golden.md`  
**Eval:** `docs/ai-evolution/evals/001-AUTH-TOKEN-REFRESH.md`  
**Contract:** `analysis.v1`

## User (abbreviated)

Automate refresh of access token with valid refresh token; prefer reuse.

## Assistant (analysis excerpt — approved shape)

```yaml
request_id: AUTH-TOKEN-REFRESH
summary: >
  Refresh via existing FakeAuthApi.RefreshToken; feature TokenRefresh may exist
  with @ignore and missing step bindings.
proposed_coverage:
  positive:
    - Valid lab-refresh-* token returns new access token
  negative:
    - Empty or invalid refresh → INVALID_REFRESH
  edge:
    - Do not confuse lab-token-* (access) with lab-refresh-* (refresh)
assumptions:
  - API-only; LoginResponse is the refresh response DTO
open_questions:
  - Add Scenario Outline for invalids or one negative scenario?
out_of_scope:
  - GetProfile
evidence:
  - path: labs/csharp-reqnroll-lab/src/AutomationLab/Clients/AuthApiClient.cs
    reason: RefreshToken contract
  - path: labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features/TokenRefresh.feature
    reason: Existing planned feature
meta:
  target: labs/csharp-reqnroll-lab
  domain: Auth
  contract: analysis.v1
  already_covered: false
```

## Why this is approved

Cites real paths, does not invent a new Auth service, separates facts from questions.
