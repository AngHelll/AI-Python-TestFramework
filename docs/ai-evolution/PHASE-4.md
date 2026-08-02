# Fase 4 — Tools registry (read-only)

**Fecha:** 2026-07-30  
**Estado:** v1 entregada — registry + runner + smoke 6/6  
**Precondiciones:** [Fase 0](PHASE-0-COMPLETE.md) · [Fase 1](PHASE-1.md) · [Fase 2–3](PHASE-2-3.md)

---

## Objetivo

Que la IA **investigue con herramientas confiables y auditables**, sin shell arbitrario ni escritura.

---

## Entregables

| Entregable | Path |
|------------|------|
| Registry manifest | `tools/registry/v1/registry.json` |
| Permissions matrix | `tools/registry/v1/PERMISSIONS.md` |
| Runner CLI | `scripts/tools_runner.py` |
| Finder (kinds filter) | `scripts/find_existing_components.py` |
| Smoke | `python3 scripts/tools_runner.py smoke` |

---

## Uso obligatorio para agentes

```bash
# Listar
python3 scripts/tools_runner.py list

# Antes de create_only_if_needed
python3 scripts/tools_runner.py invoke find_existing_builder \
  --arg target=csharp --arg terms=LoginRequestBuilder --json

python3 scripts/tools_runner.py invoke find_existing_validator \
  --arg target=csharp --arg terms=LoginResponse

python3 scripts/tools_runner.py invoke search_similar_automation \
  --arg target=csharp --arg terms=AUTH-LOGIN-NEG

python3 scripts/tools_runner.py invoke detect_forbidden_patterns \
  --arg target=csharp
```

Pegar paths de `result.hits` en `evidence` de `plan.v1` / `analysis.v1`.

---

## Criterios de salida

- [x] Registry versionado con allowlist de tools/params
- [x] Entrypoint único (`tools_runner.py`)
- [x] Validación de argumentos (enum, charset, bounds)
- [x] Audit log de invocaciones
- [x] Denied: shell / write / network / secrets / push
- [x] Smoke 6/6
- [x] Retrieval eval sigue en 8/8 @k=5
- [ ] CI job opcional (`smoke` + `eval_retrieval`)
- [ ] MCP wrapper (Fase 9 del roadmap — no ahora)

---

## Relación con el workflow

| Workflow tool (spec) | Registry name |
|----------------------|---------------|
| find_existing_builder | `find_existing_builder` |
| find_existing_validator | `find_existing_validator` |
| find_reusable_step | `find_reusable_step` |
| search_similar_automation | `search_similar_automation` |
| inspect_service_contract | `inspect_service_contract` |
| detect_forbidden_patterns | `detect_forbidden_patterns` |
| validate_naming | `validate_naming` |
| get_changed_files | `get_changed_files` |
| (knowledge search) | `find_knowledge` |

Jira/XRay: aún stubs — no hay tools de red.

---

## Siguiente

Fase 5: workflow ejecutable con tracing JSON (Analyst→Planner + `tools_invoked[]` desde audit).
