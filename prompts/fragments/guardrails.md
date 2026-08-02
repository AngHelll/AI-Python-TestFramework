# Fragment — guardrails checklist (Gate 1 / Gate 2)

Copy into the run record; every unchecked item blocks approval.

- [ ] Searched existing Builder/Validator/Step (evidence paths listed)
- [ ] No real secrets or production credentials proposed
- [ ] No fixed sleeps proposed
- [ ] No removal/weakening of assertions
- [ ] Inferences labeled as assumptions, not facts
- [ ] Evidence paths listed
- [ ] Plan-only runs do not include patches
- [ ] Correct target (`labs/csharp-reqnroll-lab` vs python root)
- [ ] AUTH-DUPLICATE-BUILDER / login payload → `LoginRequestBuilder` only
- [ ] "Already covered" allowed when feature/tag already exists

Source: `knowledge/review-checklists/guardrails.md`
