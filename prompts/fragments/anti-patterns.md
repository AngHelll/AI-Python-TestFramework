# Fragment — anti-patterns (include in Analyst + Planner system context)

Never recommend or silently introduce:

| ID | Anti-pattern |
|----|----------------|
| AP-01 | Duplicate Builder (e.g. second login request builder) |
| AP-02 | Raw asserts in steps when a Validator exists |
| AP-03 | Fixed `Thread.Sleep` / `time.sleep` on happy path |
| AP-04 | Retries that swallow assertion failures |
| AP-05 | Real environment secrets / hard-coded prod credentials |
| AP-06 | Code without search evidence or approved plan |
| AP-07 | Claiming "component does not exist" without search evidence |
| AP-08 | Shared mutable static state across scenarios |
| AP-09 | Removing or weakening assertions to make tests pass |
| AP-10 | Self-approval of the same model's own patch as sole review |

Full detail: `knowledge/anti-patterns/anti-patterns.md`
