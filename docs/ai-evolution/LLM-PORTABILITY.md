# Portabilidad de LLM — local, hosteado, proveedor

**Pregunta:** ¿Podremos cambiar el modelo (Copilot ↔ Cursor ↔ Ollama ↔ Azure/OpenAI) sin rehacer el lab?  
**Respuesta corta:** **Sí**, si mantenemos la frontera actual: **LLM propone / razona; tools + gates ejecutan y autoritan.**

---

## 1. Qué es estable (no cambia con el LLM)

```text
                    ┌─────────────────────────────┐
  Cualquier LLM ──► │ Agents / prompts / contracts│  (texto)
                    └─────────────┬───────────────┘
                                  │ pide tools
                                  ▼
                    ┌─────────────────────────────┐
                    │ tools_runner / MCP / .NET   │  (allowlist)
                    │ workflow · review · patch   │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                           Gates humanos 1/2/3
```

Contratos estables:

| Pieza | Por qué importa |
|-------|-----------------|
| `analysis.v1` / `plan.v1` | I/O de agentes, independiente del vendor |
| `tools/registry/v1` | Única puerta a búsqueda/propose |
| `patch` recipes + Gate3 | No diffs libres sin allowlist |
| MCP `invoke_lab_tool` / `choose_gate2_recipe` | Mismo bridge para Cursor u otro host |
| POC .NET `LabToolGateway` | Transfer laboral sin reimplementar retrieval |

Si un LLM nuevo solo **habla el mismo contrato** y **solo llama tools allowlisteadas**, el swap es de *host*, no de *plataforma*.

---

## 2. Tres familias de LLM (futuro)

| Familia | Ejemplos | Encaje |
|---------|----------|--------|
| **Proveedor SaaS (IDE)** | GitHub Copilot, Cursor | Camino principal del runbook; cero key propia |
| **Proveedor API** | OpenAI, Azure OpenAI, Anthropic | POC SK / `--llm`; CI opcional; necesita key/endpoint |
| **Local / hosteado** | Ollama, LM Studio, vLLM, Azure AI local | Side o intranet; misma fachada “chat completions” o MCP |

### Copilot / Cursor (recomendado ahora)

- Ya tienes agents/prompts en `.github/`.
- El modelo viene con la suscripción.
- Tools: el humano (o Cursor MCP) ejecuta `tools_runner`.

### API (OpenAI / Azure)

- Hoy: `OPENAI_API_KEY` en `gate2_recipe_chat.py --llm`; Azure en host .NET `ChatOptions`.
- Útil para demos SK y automatizar *elección* de recipe con modelo.
- **No** sustituye Gate3 ni allowlists.

### Local / hosteado (futuro viable)

Condiciones para alinear sin reescritura:

1. **Adapter fino** `ChatClient` (OpenAI-compatible): Ollama suele exponer `/v1/chat/completions`.
2. Mismos system prompts / contracts (`analysis.v1`, recipe JSON schema).
3. Tools **solo** vía MCP o `tools_runner` (el modelo local no escribe al disco “por su cuenta”).
4. Eval smoke: mismos fixtures UC-05 / duplicate-builder / recipe chooser.

Qué **no** hacer con local:

- Saltar allowlist porque el modelo “corre en casa”.
- Auto-apply patches.
- Mezclar un modelo local no evaluado en CI como único Gate.

---

## 3. Matriz de cambio (esfuerzo)

| Cambio | Esfuerzo | Qué tocas |
|--------|----------|-----------|
| Copilot ↔ Cursor | Bajo | Misma knowledge; MCP en Cursor |
| Añadir Azure OpenAI al script Python `--llm` | Bajo–medio | Env + cliente HTTP (como .NET ya hace) |
| Ollama OpenAI-compatible | Bajo | `OPENAI_BASE_URL=http://localhost:11434/v1` + key dummy |
| Modelo custom sin API OpenAI | Medio | Adapter en bridge; mismos contratos |
| LangGraph / multi-agent cloud | Alto | Solo si hace falta estado/reanudación (ADR-002) |

---

## 4. Diseño para no pintar contra la pared

**Hacer**

- Seguir emitiendo YAML/JSON de contrato, no prosa suelta como única entrega.
- Invocar tools por nombre de registry.
- Gates humanos documentados (timing ya medido).

**Evitar**

- Lógica de negocio solo dentro del prompt del vendor.
- Diffs generados por LLM fuera de `recipes/`.
- Acoplar agents a APIs propietarias de un solo IDE.

**Side project (si quieres local ya)**

Repo o carpeta mínima: cliente OpenAI-compatible → llama `choose_gate2_recipe` / `tools_runner` por CLI o MCP. El lab permanece la fuente de allowlists.

---

## 5. Criterio de “listo para cambiar de LLM”

- [ ] Mismos evals 005–015 en verde sin el modelo nuevo.
- [ ] Un request tipado (p. ej. AUTH-TOKEN-REFRESH) produce `analysis.v1` + `plan.v1` válidos con el nuevo host.
- [ ] Recipe chooser: skip en duplicate; propose allowlisted en token-refresh.
- [ ] Ningún apply sin `--gate3-approved`.

---

## 6. Relación con ADR-002

ADR-002 ya fija: Cursor/scripts ahora; SK/.NET para transfer; MCP cuando hay ≥2 clientes (cumplido).  
Este doc añade: **el LLM es pluggable**; la API estable es registry + contracts + gates.

Reabrir ADR solo si un host exige bypassear `tools_runner` o auto-merge.
