# Runbook Copilot / IDE — workflow Analyst → Gate3

**Para quién:** QAs y admin/leads que automatizan o mantienen en el **IDE** (Cursor o VS + GitHub Copilot).  
**Objetivo de la prueba inicial:** que el workflow agentico sea **visible**, enseña prácticas (Reuse Before Create, evidencia, gates) y **reduce fricción** al contexto correcto — no que un job “haga magia” solo.

**Éxito ahora (acordado):** eficiencia = entregar automatización con menos fricción y mejor uso de contexto (QA); admin usa agentes distintos sin inflar prompts. **Gates humanos**, sin autonomía total. Métricas de tiempo/tokens = [log manual](evals/manual-value-log.md) · criterios en [VALUE-AND-KPIS.md](VALUE-AND-KPIS.md).

**Principio:** el LLM (Copilot/Cursor) **razona y guía**; los scripts allowlisteados + **gates humanos** son la autoridad.  
**Sin** `OPENAI_API_KEY` propia: el modelo viene del IDE/suscripción.

| Rol | Agent | Prompt |
|-----|-------|--------|
| Analyst | `.github/agents/automation-analyst.agent.md` | `.github/prompts/automation-analyst.prompt.md` |
| Planner | `automation-planner` | `automation-planner.prompt.md` |
| Builder | `automation-builder` | `automation-builder.prompt.md` |
| Reviewer | `automation-reviewer` (+ stability/xray/security) | `automation-reviewer.prompt.md` |

Contratos: `knowledge/agents/contracts.md` · Handoffs: `knowledge/agents/handoffs.md` · LLM swap: [LLM-PORTABILITY.md](LLM-PORTABILITY.md).

---

## Por qué IDE primero (y job después)

```text
HOY (dogfood QA)                    MAÑANA (opcional)
─────────────────                   ─────────────────
IDE: chat agent visible      →      Job CI: smokes / retrieval
Humano ve Gates 1/2/3        →      Job no sustituye gates de decisión
Contexto: knowledge + tools  →      Mismos scripts en pipeline
Aprende prácticas IA         →      Escala repetición mecánica
```

| | **IDE (prueba actual)** | **Job automático (futuro)** |
|--|-------------------------|-----------------------------|
| Qué optimiza | Acceso del QA al contexto, checklist, reuso | Regresión, evals, no olvidar smokes |
| Qué NO hace | Merge solo, apply sin Gate 3 | Decidir producto / skip review humana |
| Éxito | QA completa un request con evidencia y menos fricción de contexto; admin mantiene con agentes acotados | `run_all_smokes` + (luego) detector cobertura con Gate humano |

La idea inicial **no** es ocultar el flujo en un batch: es **mostrar** Analyst → Planner → Builder → Reviewer para que el **área** interiorice el método.

Tras cada historia dogfood: una fila en [evals/manual-value-log.md](evals/manual-value-log.md) (tiempo, agentes usados, sensación de contexto/tokens).

---

## Qué gana un QA en el IDE

1. **Contexto acotado** — agents cargan catálogo, anti-patterns, contracts; no “todo el monorepo a ciegas”.
2. **Tools allowlisteadas** — `find_existing_builder` antes de inventar un Builder gemelo.
3. **Entregables iguales** — siempre `analysis.v1` / `plan.v1` (comparables, rehechos).
4. **Frenos explícitos** — `already_covered`, review high → stop; Gate 3 solo humano.
5. **Misma práctica en C# o Python** — `target=csharp` apunta al lab Reqnroll.

---

## Quickstart A — Cursor (este repo)

1. Abrir carpeta **`AI-Python-TestFramework`** (raíz del repo).
2. Settings → MCP → habilitar **`ai-python-lab`** (tras `bash scripts/setup_cursor_mcp.sh` si hace falta).
3. En chat, pedir el rol (o abrir el agent file) y un request, p. ej. `AUTH-TOKEN-REFRESH`.
4. Usar MCP / terminal para tools:

```bash
python3 scripts/tools_runner.py invoke find_existing_builder \
  --arg target=csharp --arg terms=TokenRefresh --arg limit=5 --json
```

5. Guardar YAML de analysis/plan en el chat o en `artifacts/`; anotar Gate 1/2.
6. Post–Gate2: MCP `choose_gate2_recipe` o:

```bash
python3 scripts/gate2_recipe_chat.py choose \
  --request-id AUTH-TOKEN-REFRESH --terms "access token" --propose
```

---

## Quickstart B — Visual Studio / VS Code + Copilot (C#)

### Lab twin (hoy)

1. Abrir el mismo repo (o multi-root con `labs/csharp-reqnroll-lab`).
2. Copilot Chat → elegir / pegar instrucciones del agent **`automation-analyst`** (archivo en `.github/agents/`).
3. Indicar: *target C# lab, Reqnroll, Reuse Before Create*.
4. En **Terminal** integrado, mismos comandos `python3 scripts/tools_runner.py …` (Python 3 en PATH).
5. Opcional — host .NET aledaño (orquestación tipada, sin reimplementar búsqueda):

```bash
cd ../ai-automation-orchestration
export LAB_ROOT="$(cd .. && pwd)/AI-Python-TestFramework"   # ajusta a tu clone local
dotnet run --project src/AiAutomation.Orchestration -- analyze \
  --request-id AUTH-DUPLICATE-BUILDER --terms LoginRequestBuilder
dotnet run --project src/AiAutomation.Orchestration -- recipe-chat \
  --request-id AUTH-TOKEN-REFRESH --terms "access token" --propose
```

### Monorepo laboral (más adelante)

- Copiar/adaptar `.github/agents` + `prompts/contracts` al repo de trabajo.
- Apuntar `LAB_ROOT` / MCP al árbol real **o** re-hospedar `tools_runner` allí.
- **No** clonar el monorepo dentro de este lab.

---

## 0. Preparar request

```bash
# Atajo deterministic (sin chat) — útil para demos / CI
python3 scripts/workflow_runner.py start \
  --from tools/workflow/v1/samples/AUTH-TOKEN-REFRESH.json
# En real: sin --auto-gates; gates manuales
```

Campos: `request_id`, `description`, `domain`, `target` (`csharp` \| python), `terms`, `constraints`.

---

## 1. Analyst → Gate 1 (visible en el chat)

1. Agent **`automation-analyst`**.
2. Exigir YAML `analysis.v1` + evidence.
3. Tools:

```bash
python3 scripts/tools_runner.py invoke find_existing_builder \
  --arg target=csharp --arg terms=<terms> --arg limit=5 --json
python3 scripts/tools_runner.py invoke find_knowledge \
  --arg target=knowledge --arg terms=component-catalog --arg limit=5 --json
```

4. **Gate 1 (QA/humano):** approve / reject en el hilo o nota.  
   Si `already_covered: true` → **STOP**.

---

## 2. Planner → Gate 2

1. Agent **`automation-planner`** + analysis aprobado.
2. Exigir `plan.v1` (reuse, create_only_if_needed, risks).
3. **Gate 2 (humano).**

```bash
python3 scripts/gate2_recipe_chat.py choose \
  --request-id <REQUEST_ID> --terms "<terms>" --propose
```

---

## 3. Builder → Reviewer

```bash
python3 scripts/tools_runner.py invoke propose_patch \
  --arg recipe=<allowlisted-id> --json
python3 scripts/tools_runner.py invoke review_diff \
  --arg path=.forgeone/runs/patches/<proposal_id>.diff --json
```

High severity → no apply.

---

## 4. Gate 3 → apply (solo humano)

```bash
python3 scripts/patch_pipeline.py apply \
  --proposal-id <id> --gate3-approved [--run-tests]
```

Sin merge/push por agentes.

---

## 5. Demos rápidas

| Demo | Comando |
|------|---------|
| E2E choose+propose | `bash scripts/demo_gate2_recipe_flow.sh` |
| Smokes | `bash scripts/run_all_smokes.sh` |
| Timing humano | `bash scripts/run_human_sessions.sh qa-reviewer` |
| Host .NET smoke | `dotnet run … -- smoke` (repo aledaño) |

---

## 6. Mapa mental IDE

```text
  QA en Cursor / VS
        │
        │  chat: Analyst → Planner → Builder → Reviewer
        │  (ve cada artefacto y cada gate)
        ▼
  Terminal / MCP / LabToolGateway (.NET)
        │
        ▼
  tools_runner · recipes · csharp-reqnroll-lab
        │
        ▼
  Gate 3 humano → apply opcional
```

Job CI futuro = misma capa inferior (smokes/evals), **no** reemplazo del aprendizaje en IDE.
