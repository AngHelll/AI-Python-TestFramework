# Blueprint portable — de few-shot a plataforma gobernada

**Audiencia:** un agente (o humano) que debe **crear o insertar** esta práctica en **otro repositorio**, alinearla a las convenciones de ese repo, y generar los artefactos de soporte.

**Fuente de verdad de referencia:** este lab (`AI-Python-TestFramework`) — fases 0–8 + transfer POC.  
**No copiar:** stacks, nombres de builders, paths del lab C#, secretos, ni monorepos laborales.

---

## 1. Idea en una frase

Pasar de *“prompt + ejemplos → código variable”* a una **plataforma Context-First** donde el LLM **razona bajo contratos**, las **tools allowlisteadas** aportan evidencia, y **humanos aprueban en gates** — sin autonomía silenciosa.

```text
AS-IS (few-shot)                         TO-BE (plataforma)
─────────────────                        ──────────────────
Prompt largo + 2–3 ejemplos      →       Knowledge + fragments + contracts
Código directo “a ver qué sale”  →       Analyst → Gate1 → Planner → Gate2
                                         → Builder(propose) → Reviewer → Gate3
Sin evidencia de reuso           →       Reuse Before Create (tools + catalog)
Sin métrica comparable           →       Evals + goldens + smokes
Acoplado a un chat/vendor        →       LLM pluggable; registry estable
```

---

## 2. Invariantes (no negociables)

Cualquier inserción en otro repo **debe** conservar:

| # | Invariante |
|---|------------|
| I-1 | **LLM propone / razona; tools + gates ejecutan y autorizan** |
| I-2 | Salidas tipadas (`analysis.v1`, `plan.v1`) — no solo prosa |
| I-3 | **Reuse Before Create** — buscar antes de inventar componentes |
| I-4 | **Plan Before Code** — no patches en fase Analyst/Planner |
| I-5 | Gates humanos 1 (análisis), 2 (plan), 3 (apply) |
| I-6 | Tools solo vía **registry allowlist** (sin shell arbitrario) |
| I-7 | Apply de patches solo con flag explícito de Gate 3 |
| I-8 | Ningún agente hace merge/push ni aprueba solo su propio cambio |
| I-9 | Knowledge y ejemplos canónicos los **promueve un humano**, no el LLM |
| I-10 | El host del LLM (Copilot / Cursor / API / local) es **intercambiable** |

Si el repo destino exige saltarse I-5–I-8, **detener** e informar — no “adaptar” quitando gates.

---

## 3. Modelo de capas (stack-agnóstico)

```text
┌─────────────────────────────────────────────────────────────┐
│  SURFACES (IDE)                                             │
│  agents/ · prompts/ · rules · MCP (opcional)                │
└───────────────────────────┬─────────────────────────────────┘
                            │ mismos contratos
┌───────────────────────────▼─────────────────────────────────┐
│  CONTRACTS + FRAGMENTS                                      │
│  analysis.v1 · plan.v1 · guardrails · anti-patterns · gates │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  KNOWLEDGE (gobernada)                                      │
│  catalog · patterns · ADRs · examples · review taxonomy     │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  TOOLS (deterministas, allowlist)                           │
│  find_* · validate_* · review_diff · propose_patch          │
│  workflow_runner · patch_pipeline (apply = Gate3 only)      │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  TARGET CODE (sujeto)                                       │
│  El framework real del repo destino (POM, BDD, API, etc.)   │
│  Opcional: lab gemelo reducido si no se toca el monorepo    │
└─────────────────────────────────────────────────────────────┘
```

**Regla de transferencia:** el **sujeto** (código de tests) y la **plataforma IA** se separan. En este lab, el sujeto espejo es `labs/csharp-reqnroll-lab/`; en el destino puede ser el propio árbol de tests.

---

## 4. Roles y handoff

| Rol | Produce | No hace | Siguiente |
|-----|---------|---------|-----------|
| **Analyst** | `analysis.v1` + evidence | Código, plan técnico, patches | Gate 1 → Planner |
| **Planner** | `plan.v1` + reuse/create | Patches, merge | Gate 2 → Builder (o stop si `already_covered`) |
| **Builder** | Propuesta de patch (recipe / propose) | Apply sin Gate 3 | Reviewer |
| **Reviewer** (+ sub: stability / tags / security) | Findings con códigos | Auto-fix, approve solo | Gate 3 |
| **Humano** | Approve/reject gates | — | Apply / stop / feedback a knowledge |

Diagrama mínimo:

```text
Request → Analyst → [Gate 1] → Planner → [Gate 2]
        → Builder(propose) → Reviewer → [Gate 3] → apply → STOP
```

---

## 5. Inventario de artefactos a crear

Al insertar en un repo destino, crear **como mínimo** lo marcado ★; el resto según madurez.

### 5.1 Documentación de evolución ★

| Artefacto | Propósito |
|-----------|-----------|
| `docs/ai-evolution/README.md` | Índice |
| `docs/ai-evolution/00-vision-and-baseline.md` | As-is few-shot → to-be; in/out scope |
| `docs/ai-evolution/01-use-cases.md` | UC priorizados + historias golden |
| `docs/ai-evolution/02-risks.md` | Riesgos + “IA nunca sin humano” |
| `docs/ai-evolution/workflow-*-*.md` | Spec Analyst→Planner (y Builder/Reviewer) |
| `docs/ai-evolution/PORTABLE-BLUEPRINT.md` | Este doc (o enlace) |
| `docs/ai-evolution/LLM-PORTABILITY.md` | Swap de host/modelo |
| `docs/ai-evolution/evals/` + `RUBRIC.md` | ≥3–5 historias few-shot vs workflow |

### 5.2 Contratos y fragments ★

| Artefacto | Propósito |
|-----------|-----------|
| `prompts/contracts/analysis.v1.yaml` | I/O Analyst |
| `prompts/contracts/plan.v1.yaml` | I/O Planner |
| `prompts/fragments/guardrails.md` | Límites |
| `prompts/fragments/anti-patterns.md` | Qué no generar |
| `prompts/fragments/gate-criteria.md` | Criterios Gate 1/2 (y 3) |
| `prompts/fragments/context-load-order.md` | Orden de carga de contexto |
| `prompts/examples/approved/` | 2–3 goldens humanos |

### 5.3 Knowledge ★

```text
knowledge/
├── README.md
├── agents/contracts.md
├── agents/handoffs.md
├── framework/component-catalog.md    # inventario REAL del destino
├── patterns/approved-patterns.md
├── anti-patterns/anti-patterns.md
├── coding-standards/naming.md
├── review-checklists/guardrails.md
├── examples/                         # analyses/plans canónicos
├── decisions/ADR-001-*.md            # al menos: separación plataforma/sujeto
├── decisions/ADR-002-*.md            # orquestación / tools entrypoint
└── known-issues/                     # trampas de eval del destino
```

**Adaptación:** renombrar carpetas de dominio (`api/`, `bdd/`, `xray/`, etc.) a lo que el repo destino use. El **catálogo** debe listar componentes **existentes**, no inventados.

### 5.4 Agents / prompts de superficie ★

| Pieza | Ejemplo de path (ajustar a la convención del destino) |
|-------|--------------------------------------------------------|
| Agent Analyst | `.github/agents/…-analyst.agent.md` o `.cursor/rules/` / agents Cursor |
| Agent Planner | idem |
| Agent Builder | idem (solo propose) |
| Agent Reviewer | idem (+ subreviewers si aplica) |
| Prompts espejo | `.github/prompts/` o `prompts/library/` |
| Rule corta | `.cursor/rules/ai-evolution.mdc` (o equivalente) |

**Least privilege:** tools del agent = `read` / `search` / (edit solo Builder con límites). Preferir invocar CLI registry que dar shell libre.

### 5.5 Tools registry (Fase tools) ★ para madurez ≥ “tools”

| Artefacto | Propósito |
|-----------|-----------|
| `tools/registry/v1/registry.json` | Manifest allowlist |
| `tools/registry/v1/PERMISSIONS.md` | Denied: shell, write libre, network, secrets, git_push |
| `scripts/tools_runner.py` (o equivalente) | Única puerta `list` / `invoke` / `smoke` |
| Tools mínimas | `find_existing_*`, `search_similar_*`, `find_knowledge`, `detect_forbidden_patterns`, `validate_naming` |

### 5.6 Workflow + patches (madurez avanzada)

| Artefacto | Propósito |
|-----------|-----------|
| `scripts/workflow_runner.py` | Runs trazados Analyst→Planner |
| `tools/workflow/v1/` | Schema + samples |
| `tools/patches/v1/allowlist.json` | Rutas permitidas |
| `tools/patches/v1/recipes.json` + `recipes/*.diff` | Cuerpos deterministas |
| `scripts/patch_pipeline.py` | propose / review / apply `--gate3-approved` |
| `scripts/review_diff.py` | Taxonomía de findings |
| MCP opcional | Wrapper stdio sobre `tools_runner` — **sin** apply |

### 5.7 Evals y smokes ★

| Artefacto | Propósito |
|-----------|-----------|
| `docs/ai-evolution/evals/00N-….md` | Historias con score few-shot vs workflow |
| ≥1 trampa de reuso | Pedir componente que **ya existe** → debe reusar |
| ≥1 already_covered | Debe parar sin Builder |
| `scripts/run_all_smokes.sh` | Entrypoint CI/local |
| Log manual de valor | Tiempo/fricción (no dashboard obligatorio al inicio) |

---

## 6. Contratos mínimos (copiar y adaptar campos de dominio)

### `analysis.v1` (campos requeridos)

- `request_id`, `summary`
- `proposed_coverage`: `positive` / `negative` / `edge`
- `assumptions`, `open_questions`, `out_of_scope`
- `evidence[]`: `{ path, reason }` (min 1 tras búsqueda)
- `meta.already_covered` (opcional pero crítico)

### `plan.v1` (campos requeridos)

- `request_id` (= analysis aprobado)
- `reuse`: builders / validators / steps / pages_or_clients *(renombrar a tipos del destino)*
- `create_only_if_needed[]` con justificación
- `files_likely_affected[]` paths concretos
- `risks[]`: `{ id, severity, note }`
- `implementation_steps[]` (ordenados, sin código completo)
- `evidence[]`
- `policy_checks.searched_before_create` (true si hay create)

**Versionado:** breaking → `analysis.v2.yaml`; no borrar v1 mientras evals lo citan.

---

## 7. Fases de adopción (en el repo destino)

No instalar F7/F8 el día 1. Secuencia recomendada:

| Fase | Nombre | Entrega | Criterio de salida |
|------|--------|---------|-------------------|
| **A0** | Visión + baseline | Vision, UC, riesgos, 3–5 historias as-is few-shot puntuadas | Documento de cierre |
| **A1** | Contratos + fragments | `analysis.v1` / `plan.v1` + guardrails | Un análisis humano-aprobado en el formato |
| **A2** | Knowledge v0 | Catalog + patterns + anti-patterns del **destino** | Catálogo refleja árbol real |
| **A3** | Agents Analyst/Planner | Agents + prompts + Gate 1/2 criteria | 2 runs con evidence |
| **A4** | Tools read-only | Registry + find_* + smoke | Agents solo invocan registry |
| **A5** | Evals formales | Rubric + goldens + trampa duplicate | Workflow ≥ few-shot en score |
| **A6** | Reviewer | Taxonomía + `review_diff` fixtures | UC de sleep/dup/tags (o equivalentes) |
| **A7** | Patch pipeline | Recipes + allowlist + Gate 3 | Apply imposible sin flag |
| **A8** | Surfaces + CI smokes | IDE agents + `run_all_smokes` | Smokes verdes en CI opcional |
| **A9** | Transfer/host | MCP / gateway otro lenguaje | Mismo registry, sin reimplementar búsqueda |

Mapeo a este lab: A0≈F0 … A8≈F8, A9≈F9.

---

## 8. Playbook para el agente instalador

Usar este bloque como system/task prompt al agente que trabaja **en el repo destino**.

### 8.1 Misión

> Inserta la plataforma de automatización gobernada (Context-First, Analyst→Planner→Builder→Reviewer, human gates) alineada a las prácticas **ya existentes** de este repositorio. Evoluciona desde few-shot prompting; no reemplaces el framework de tests — añádele gobernanza IA.

### 8.2 Pasos obligatorios (orden)

1. **Inventariar el destino** (read-only):
   - Lenguaje(s), runner de tests, POM/BDD/API layers
   - Dónde viven pages/builders/validators/steps/features
   - Convenciones de naming, tags (XRay/Allure/…), secrets
   - Surfaces IA ya existentes (`prompts/`, `.github/agents/`, `.cursor/`, etc.)
2. **Mapear vocabulario** few-shot → plataforma:
   - Extraer anti-patterns reales del código/docs
   - Listar 5–15 componentes reutilizables → semilla de `component-catalog.md`
3. **Elegir fase objetivo** (default: completar A0–A3; proponer A4+).
4. **Crear árbol de artefactos** de §5 sin inventar componentes de producción.
5. **Alinear paths** a la convención del destino (no forzar `labs/csharp-reqnroll-lab/`).
6. **Escribir 3 historias golden** del dominio real (anonimizadas):
   - 1 happy path nuevo
   - 1 already_covered
   - 1 trampa de duplicado
7. **Baseline few-shot:** documentar score as-is (aunque sea cualitativo 0–10).
8. **Smoke mínimo:** checklist o script que valide contracts/files presentes.
9. **ADR corto:** por qué registry + gates; qué queda fuera (merge, LangGraph, etc.).
10. **Stop** y pedir Gate humano antes de cualquier apply/patch al código de tests.

### 8.3 Reglas de alineación

| Situación en destino | Acción |
|----------------------|--------|
| Ya hay `prompts/context/` few-shot | Conservar; añadir `contracts/` + `knowledge/` al lado; fragments apuntan a ambos |
| Solo Copilot o solo Cursor | Crear surface nativa; contracts idénticos |
| No hay CI | `run_all_smokes.sh` local primero; CI después |
| Monorepo sensible | Plataforma en carpeta dedicada o repo aledaño; **lab gemelo sintético** si no se puede tocar prod |
| Naming distinto (Factory vs Builder) | Renombrar campos de `plan.v1.reuse` y tools `find_*` al vocabulario local |
| Ya hay linters/hooks | Reviewer taxonomy mapea a reglas existentes; no duplicar en silencio |

### 8.4 Qué no hacer

- No clonar el lab C# completo “porque sí”.
- No copiar recipes/diffs de otro dominio.
- No exponer `apply` por MCP.
- No auto-promover salidas LLM a `examples/approved/`.
- No afirmar cobertura Jira/XRay sin evidencia.
- No saltar Gate 2 “porque el plan es obvio”.

### 8.5 Definition of Done (inserción A0–A3)

- [ ] Vision + riesgos + UC en `docs/ai-evolution/`
- [ ] Contratos `analysis.v1` / `plan.v1` + fragments
- [ ] `knowledge/` con catálogo **verificado** contra el árbol
- [ ] Agents Analyst + Planner (Builder/Reviewer stub OK)
- [ ] Gate criteria documentados
- [ ] ≥3 eval stubs con baseline few-shot
- [ ] ADR de orquestación
- [ ] README índice + “cómo correr el primer request”
- [ ] Humano revisó que paths/naming coinciden con el repo

---

## 9. Checklist de adaptación rápida (tabla)

| Concepto en este lab | Pregunta en destino | Resultado |
|----------------------|---------------------|-----------|
| `LoginRequestBuilder` | ¿Cómo se llaman los builders/factories? | Entrada de catálogo |
| Reqnroll Feature | ¿Behave / SpecFlow / Playwright fixtures / pytest? | Target tree + load order |
| `Thread.Sleep` | ¿Cuál es el anti-patrón de wait local? | Anti-pattern + detect tool |
| Tags `@Xray` | ¿Tags / links de trazabilidad? | Reviewer XRay-equivalente |
| `target=csharp\|python` | ¿Un target o N módulos? | Args de tools |
| `.forgeone/runs/` | ¿Dónde auditar invocaciones? | Path gitignored |
| Gate3 `--gate3-approved` | ¿Flag CLI equivalente? | Misma semántica |

---

## 10. Métrica de éxito (temprana)

No hace falta dashboard. Tras 2–3 historias:

| Señal | Few-shot | Plataforma |
|-------|----------|------------|
| Reuso citado con path | Raro | Obligatorio en evidence |
| Duplicados propuestos | Frecuente | Trampa eval = FAIL |
| Tiempo a plan revisable | Variable | Gate 1/2 con artefacto YAML |
| Fricción de contexto | Prompt gigante | Fragments + catalog |
| Apply accidental | Posible | Bloqueado sin Gate 3 |

Registrar filas en un `evals/manual-value-log.md` (tiempo, sensación de contexto, agentes usados).

---

## 11. Relación con este repositorio

| Doc local | Usar como |
|-----------|-----------|
| [00-vision-and-baseline.md](00-vision-and-baseline.md) | Ejemplo de A0 |
| [LLM-PORTABILITY.md](LLM-PORTABILITY.md) | Frontera LLM/tools |
| [COPILOT-RUNBOOK.md](COPILOT-RUNBOOK.md) | Flujo IDE humano |
| [PHASE-9-TRANSFER-POC.md](PHASE-9-TRANSFER-POC.md) | Host .NET / MCP |
| `knowledge/agents/contracts.md` | Roles |
| `prompts/contracts/*.yaml` | Schemas a clonar |
| `tools/registry/v1/` | Modelo de allowlist |

**Plantilla de prompt lista para pegar:** [bootstrap/INSTALLER-AGENT.prompt.md](bootstrap/INSTALLER-AGENT.prompt.md)

---

## 12. Resumen ejecutivo

Esta evolución **no** es “mejor prompt”. Es un **sistema**:

1. **Contexto gobernado** (knowledge + fragments)  
2. **Contratos de salida** (analysis / plan)  
3. **Roles especializados** (sin auto-aprobación)  
4. **Tools allowlisteadas** (evidencia, no magia)  
5. **Gates humanos** (decisión)  
6. **Evals** (comparar vs few-shot y no regresar)

Un agente que inserte esto en otro repo debe **traducir**, no **clonar**: mismas invariantes, vocabulario y paths del destino, fases A0→A9 según madurez.
