# Valor y KPIs — alineación de éxito

**Estado:** criterios acordados (manual primero).  
**No** es un dashboard automático: sirve para que área/admin y QAs midan lo mismo.

---

## Definiciones alineadas

| Término | Significado **ahora** | Explicitamente **no** |
|---------|----------------------|------------------------|
| **Eficiencia** | Cada QA entrega automatización con menos fricción: workflow/agentes claros, contexto correcto, menos rework. Admin mantiene features con agentes distintos sin inflar el prompt. | $/token automático; autonomía sin humano |
| **Agentico** | Roles (Analyst→Planner→Builder→Reviewer) + tools allowlisteadas + **gates humanos 1/2/3** | Autonomía total / merge silencioso |
| **Madurez (área)** | Uso habitual de agentes en el flujo de automatización; métricas ligeras (tiempo, tokens) tomadas a mano | Plataforma “completa” o LangGraph |
| **Siguiente nivel (ejemplo)** | Tool que detecte cambios de producto/API y proponga **revisión de cobertura**; humano autoriza el plan | Auto-aplicar cobertura o saltarse Gate 2/3 |

Sensación de éxito temprana (válida): *“noto menos contexto basura / menos scroll de few-shot / más evidencia”* — aunque aún no haya CSV de tokens.

---

## Audiencias

| Quién | Qué optimiza el lab para ellos |
|-------|--------------------------------|
| **QA** | Pedir automatización vía agentes + runbook IDE; reuso y gates visibles |
| **Admin / lead** | Mantener catálogo, prompts, recipes, evals; agentes con least-privilege y contexto acotado |
| **Área (adopción)** | Que el método se use, no solo que los smokes pasen |

---

## KPIs (manual hasta otro punto)

Registrar en [evals/manual-value-log.md](evals/manual-value-log.md) o en la sesión humana.

| # | KPI | Cómo tomar (manual) | Señal buena |
|---|-----|---------------------|-------------|
| 1 | **Tiempo por automatización** | Minutos wall-clock Gate1→apply (o “plan usable”) | Baja vs few-shot previo / vs primera historia |
| 2 | **Uso de agentes** | ¿Se usó Analyst/Planner/Builder/Reviewer? (sí/parcial/no) | ≥1 historia/semana con flujo completo en el área |
| 3 | **Contexto / tokens (estimado)** | Cursor/Copilot usage o “aprox. turnos + tamaño prompt” | Menos paste de few-shot; más tool/knowledge |
| 4 | **Reuse hit** | ¿`already_covered` / builder existente detectado? | Sí cuando aplica; menos duplicados |
| 5 | **Gate discipline** | ¿Hubo Gate 1/2/3 explícitos? | Nunca apply sin Gate 3 |

Opcional más adelante (no bloquear madurez de área): export API de usage, CI de smokes, detector de cambios → plan de cobertura.

---

## Arco (sin reescribir la plataforma)

```text
HOY
  IDE + agentes + gates
  Eficiencia = fricción QA + contexto admin
  Métricas = log manual

MADUREZ ÁREA
  Varios QAs usan el runbook
  Logs de tiempo/tokens suficientes para comparar

SIGUIENTE NIVEL (ej.)
  Detector de cambios → propone coverage review
  Humano revisa plan → autoriza o no
  Mismo allowlist / mismos contratos
```

Portabilidad LLM: [LLM-PORTABILITY.md](LLM-PORTABILITY.md). Runbook: [COPILOT-RUNBOOK.md](COPILOT-RUNBOOK.md).

---

## Fuera de alcance hasta decidir KPI primario de área

- Optimizar tokens del chat a costa de más rework humano  
- Autonomía de merge/push  
- Clonar monorepo laboral aquí  
- Diffs LLM libres fuera de recipes
