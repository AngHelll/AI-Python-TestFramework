# Fragment — mandatory context load order

Load in this order (skip only if target does not apply):

1. `prompts/contracts/analysis.v1.yaml` or `plan.v1.yaml` (matching role)
2. `prompts/fragments/anti-patterns.md`
3. `prompts/fragments/guardrails.md`
4. `knowledge/framework/component-catalog.md`
5. `knowledge/patterns/mapping-python-csharp.md` (if C# lab or cross-stack)
6. `knowledge/patterns/approved-patterns.md`
7. Target tree search: Builders, Validators, Features, Steps, Clients
8. Matching golden under `knowledge/examples/` if `request_id` known
9. `knowledge/known-issues/eval-traps.md`

Record every path touched under `evidence`.
