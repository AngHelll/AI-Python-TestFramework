# Permissions matrix — Tool Registry v1

| Capability | Allowed? | How |
|------------|----------|-----|
| Read files under SEARCH_ROOTS | Yes | Via registered find_* / detect_* tools only |
| Search knowledge / prompts fragments | Yes | `find_knowledge` |
| List changed files (git status) | Yes | `get_changed_files` with prefix enum |
| Arbitrary shell / curl / rm | **No** | Denied in registry; no handler |
| Write / patch files | **No** | Phase 4 is read-only |
| Network | **No** | No handlers open sockets |
| Read `.env` / secrets | **No** | Not in SEARCH_ROOTS |
| git commit / push | **No** | Denied |
| Invoke unknown tool name | **No** | Runner rejects |

## Argument validation

- `target` / `kind` / `prefix` → enums only
- `terms` → charset + max length
- `limit` → min/max bounds
- Unknown `--arg` keys → rejected

## Audit

Each `invoke` (unless `--no-audit`) writes JSON under `.forgeone/runs/tools/` with tool name, params, hit counts, timestamp.
