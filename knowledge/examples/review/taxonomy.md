# Review findings taxonomy v1

Used by `scripts/review_diff.py` and UC-05–07 evals. Reviewer **observes only** — no auto-fix.

| Code | Category | Severity | Detects |
|------|----------|----------|---------|
| `DUP-BUILDER` | duplication | high | New `*Builder` that shadows catalog login builder (e.g. `LoginPayloadBuilder`, `LoginRequestBuilder2`) |
| `DUP-VALIDATOR` | duplication | high | Parallel `*Validator` for login response when `LoginResponseValidator` exists |
| `STAB-SLEEP-CS` | stability | high | `Thread.Sleep(` |
| `STAB-SLEEP-PY` | stability | high | `time.sleep(` |
| `STAB-RETRY-SWALLOW` | stability | medium | `catch` / `except` around assert-like failures with bare retry (heuristic) |
| `XRAY-MISSING-TAG` | xray | medium | Feature scenario without `@AUTH-*`, `@USER-*`, or `@TEST_*` style tag |
| `SEC-SECRET` | security | high | Hard-coded `password=` / `api_key=` / `secret=` literals (non-lab) |
| `ARCH-ASSERT-IN-STEP` | architecture | low | FluentAssertions / Assert in Steps when Validator type also added in same diff (heuristic) |

## Sub-reviewer lenses

Filter with `--category duplication|stability|xray|security|architecture`:

```bash
python3 scripts/review_diff.py eval --category stability
```

## Severity bands

- **high** — block Gate 3 / request human change
- **medium** — should fix before merge
- **low** — advisory

## Out of scope v1

- Full semantic clone detection
- LLM-only opinions without a rule hit
- Auto-editing the diff
