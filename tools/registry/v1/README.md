# Tool Registry v1

**Phase:** 4  
**Mode:** `read_only`  
**Entrypoint:** `python3 scripts/tools_runner.py`  
**Manifest:** [`registry.json`](registry.json)

Agents and humans must **not** invent ad-hoc shell for framework search. Use only registered tools.

## Commands

```bash
python3 scripts/tools_runner.py list
python3 scripts/tools_runner.py invoke find_existing_builder \
  --arg target=csharp --arg terms=LoginRequestBuilder --arg limit=5
python3 scripts/tools_runner.py invoke detect_forbidden_patterns --arg target=csharp
python3 scripts/tools_runner.py invoke validate_naming \
  --arg kind=builder --arg name=LoginRequestBuilder
python3 scripts/tools_runner.py smoke
```

Audit logs (gitignored): `.forgeone/runs/tools/<invocation_id>.json`

## Tools

| Tool | Purpose |
|------|---------|
| `find_existing_builder` | Builders |
| `find_existing_validator` | Validators |
| `find_reusable_step` | Steps |
| `search_similar_automation` | Features + steps |
| `inspect_service_contract` | Clients / pages |
| `find_knowledge` | knowledge + fragments |
| `detect_forbidden_patterns` | Sleep / secret-like literals |
| `validate_naming` | Naming conventions |
| `review_diff` | Review synthetic/unified diffs (UC-05–07) |
| `propose_patch` | Create patch proposal from recipe (no apply) |

## Denied (registry)

`arbitrary_shell`, `write_files`, `network`, `secrets_read`, `git_push`, `git_commit`

See [PERMISSIONS.md](PERMISSIONS.md).
