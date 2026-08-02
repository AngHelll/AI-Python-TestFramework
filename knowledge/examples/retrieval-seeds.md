# Retrieval seeds v0.2.0

Machine-readable: [`retrieval-seeds.json`](retrieval-seeds.json) (**16 cases**).

| ID | Target | Expected |
|----|--------|----------|
| login-request-builder | csharp | LoginRequestBuilder.cs |
| refresh-token-api | csharp | AuthApiClient.cs |
| token-refresh-feature | csharp | TokenRefresh.feature |
| invalid-login-scenario | csharp | Login.feature |
| get-user-profile | csharp | AuthApiClient.cs |
| user-profile-validator | csharp | UserProfileValidator.cs |
| account-lockout | csharp | Login.feature |
| login-response-validator | csharp | LoginResponseValidator.cs |
| refresh-token-data | csharp | RefreshTokenData.cs |
| python-login-page | python | pages/login_page.py |
| python-login-feature | python | features/login.feature |
| anti-sleep-flakiness | knowledge | anti-patterns.md |
| component-catalog | knowledge | component-catalog.md |
| agent-contracts | knowledge | agents/contracts.md |
| analysis-contract | knowledge | analysis.v1.yaml |
| review-taxonomy | knowledge | review/taxonomy.md |

```bash
python3 scripts/eval_retrieval.py --k 5   # 16/16
```
