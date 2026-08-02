# Transfer POC (.NET) — documentación de avance

**Estado:** en marcha (2026-07-31)  
**Repo aledaño:** `../ai-automation-orchestration`  
**ADR:** [ADR-002](../../knowledge/decisions/ADR-002-orchestration.md)

## Por qué un repo aledaño

El lab (este repo) es la plataforma Python + contratos + tools allowlisteadas.  
El transfer laboral necesita un host **.NET** que consuma esas tools sin clonar el monorepo de trabajo ni reimplementar búsqueda.

## Capas entregadas

| Capa | Qué | Verificación |
|------|-----|----------------|
| Gateway | `LabToolGateway` → `tools_runner` / `patch_pipeline` | `smoke` |
| Stubs | Analyst / Planner / Reviewer / **Builder** | handoff + propose |
| SK plugin | `LabToolsPlugin` (`lab.*` + `propose_patch`) | `sk-smoke` |
| Chat opcional | OpenAI/Azure + function calling | `chat-smoke` (**SKIP** sin key) |
| Contratos | YAML `analysis.v1` / `plan.v1` | `contracts-smoke` |
| Patch / Gate3 | propose recipes; apply solo con `--gate3-approved` | `build-smoke` **5/5** |
| Timing | `gate-timing.v1` machine vs human waits | `gate_timing.py smoke` **4/4** |
| MCP | Bridge + stdio server sobre `tools_runner` | `mcp_lab_smoke` **6/6** |
| Gate2→recipe | Chooser allowlisted → propose (no apply) | `gate2_recipe_chat` **7/7** |

## Comandos (desde el POC)

```bash
cd ../ai-automation-orchestration
dotnet run --project src/AiAutomation.Orchestration -- smoke
dotnet run --project src/AiAutomation.Orchestration -- contracts-smoke
dotnet run --project src/AiAutomation.Orchestration -- build-smoke
dotnet run --project src/AiAutomation.Orchestration -- build-propose --recipe good-access-token-expired
dotnet run --project src/AiAutomation.Orchestration -- apply --proposal-id <id> --gate3-approved --run-tests --restore-after
dotnet run --project src/AiAutomation.Orchestration -- analyze --request-id AUTH-DUPLICATE-BUILDER --out artifacts
```

## Contratos

- `prompts/contracts/analysis.v1.yaml` / `plan.v1.yaml`
- FS-03 duplicate builder: `prompts/examples/approved/03-duplicate-builder-reject.md`
- Producer: `AiAutomation.Orchestration.ContractFactory`

## Patch / Gate 3

```text
plan (already_covered?) → skip propose
           ↓ no
propose_patch (recipe allowlisted)
           ↓
review_diff → awaiting_gate3 | blocked
           ↓
apply --gate3-approved   ← humano; .NET + lab se niegan sin flag
```

Apply **no** está expuesto como KernelFunction (solo propose).

## Límites (no negociables)

- Tools solo vía allowlist del lab
- Sin merge/push silencioso
- Sin apply sin `--gate3-approved`
- Chat LLM opcional; smokes no requieren API key
- No clonar monorepo laboral aquí

## Siguiente

1. ~~Medición humana de gates/tiempos~~ → eval [013](evals/013-gate-timing.md) · `human` + [human-sessions/](evals/human-sessions/)
2. ~~MCP wrapper~~ → eval [014](evals/014-mcp-lab.md) · `tools/mcp/v1/`
3. Sesiones humanas reales + Cursor MCP local ← **listo para dogfood** (`.cursor/mcp.json`, `run_human_sessions.sh`)
4. (Opcional) chat model que elija recipe tras Gate 2

```bash
bash scripts/setup_cursor_mcp.sh
bash scripts/run_human_sessions.sh qa-reviewer
```

Eval transfer: [012](evals/012-dotnet-transfer-poc.md)
