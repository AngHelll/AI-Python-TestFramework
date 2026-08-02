---
name: find-existing-components
description: Locate existing Builders, Validators, Steps, Clients, and knowledge via the Phase 4 tools registry (read-only)
---

# Find existing components

**Required entrypoint:** `python3 scripts/tools_runner.py`  
Do not use arbitrary `rg`/`find` shell when the registry covers the need.

## Before `create_only_if_needed`

```bash
python3 scripts/tools_runner.py invoke find_existing_builder \
  --arg target=csharp --arg terms=LoginRequestBuilder --arg limit=5 --json

python3 scripts/tools_runner.py invoke find_existing_validator \
  --arg target=csharp --arg terms=LoginResponse --json

python3 scripts/tools_runner.py invoke search_similar_automation \
  --arg target=csharp --arg terms=AUTH-LOGIN-NEG --json

python3 scripts/tools_runner.py invoke find_knowledge \
  --arg target=knowledge --arg terms=component-catalog --json
```

## Other tools

```bash
python3 scripts/tools_runner.py invoke detect_forbidden_patterns --arg target=csharp
python3 scripts/tools_runner.py invoke validate_naming --arg kind=builder --arg name=FooBuilder
python3 scripts/tools_runner.py invoke get_changed_files --arg prefix=labs/csharp-reqnroll-lab
python3 scripts/tools_runner.py smoke
```

Docs: `tools/registry/v1/README.md`, `docs/ai-evolution/PHASE-4.md`.

## Evidence

Copy `result.hits[].path` into plan/analysis `evidence` with reason = tool name + terms.
