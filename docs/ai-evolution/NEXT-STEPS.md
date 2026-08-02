# Próximos pasos

- Lab F0–F8 · Transfer · MCP · humanos · Gate2 recipe chat
- **Éxito / KPIs:** [VALUE-AND-KPIS.md](VALUE-AND-KPIS.md) · log [evals/manual-value-log.md](evals/manual-value-log.md)
- **Roadmap:** [ROADMAP.md](ROADMAP.md) · **Personas:** [ADOPTION-PERSONAS.md](ADOPTION-PERSONAS.md)
- **Runbook Copilot:** [COPILOT-RUNBOOK.md](COPILOT-RUNBOOK.md)
- **Portabilidad LLM:** [LLM-PORTABILITY.md](LLM-PORTABILITY.md)

## Alineación (acordada)

| | Ahora |
|--|-------|
| Eficiencia | Menos fricción QA + contexto acotado para admin; tokens notados a mano, no dashboard |
| Agentico | Roles + tools + **gates humanos** (sin autonomía total) |
| Madurez | Uso de agentes a nivel **área** + tiempo/tokens manuales |
| Siguiente nivel (ej.) | Detector de cambios → plan de cobertura → humano autoriza |

## Cerrado (reciente)

| Ítem | Doc |
|------|-----|
| Dogfood MCP + sesiones | evals 012–014 |
| Recipe chooser post–Gate2 | eval 015 · `demo_gate2_recipe_flow.sh` |
| Runbook Copilot + swap LLM + KPIs | este índice · VALUE-AND-KPIS |

## Portar a otro repo

Idea abstraída + prompt de instalación: [PORTABLE-BLUEPRINT.md](PORTABLE-BLUEPRINT.md) · [bootstrap/INSTALLER-AGENT.prompt.md](bootstrap/INSTALLER-AGENT.prompt.md).

## Uso sin API key propia

Copilot/Cursor aportan el modelo; scripts + gates son la autoridad:

```bash
bash scripts/demo_gate2_recipe_flow.sh
# Ver COPILOT-RUNBOOK.md para el flujo agent por agent
```

## No hacer aún

- LangGraph / merge / clone monorepo / apply vía MCP  
- Diffs LLM libres / skip Gate 2–3 en “coverage bot”  
- Acoplar lógica solo a un vendor de IDE  
- Instrumentación automática de $ / tokens (después del log manual)

## Siguiente viable

1. Ensayar el runbook **en IDE** con ≥1 QA del área; registrar fila en `manual-value-log`  
2. Repetir 2–3 historias: comparar tiempo y “contexto sense” vs few-shot  
3. (Opc.) job CI = solo smokes/evals (no sustituye gates)  
4. (Más tarde) diseñar *coverage-change detector* → propose plan → Gate humano (mismo contrato)
