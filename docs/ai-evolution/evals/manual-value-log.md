# Log manual de valor (tiempo / tokens / agentes)

Una fila por historia o sesión. No requiere API key ni export automático.

| Fecha | Quién | Historia / request | Flujo agentes (A/P/B/R) | Tiempo min (G1→plan o apply) | Tokens / contexto (aprox.) | Reuse hit? | Gates OK? | Notas (fricción / win) |
|-------|-------|--------------------|-------------------------|------------------------------|----------------------------|------------|-----------|------------------------|
| | | | | | | | | |

### Cómo estimar tokens / contexto (sin telemetría)

- **Turnos** del chat (contar mensajes del modelo).  
- **Sensación:** more/same/less context paste vs few-shot.  
- Si el IDE muestra usage: anotar el delta de la sesión.  
- Preferir “usé tools/MCP + knowledge” vs “pegué 3 ejemplos largos”.

### Ejemplo

| Fecha | Quién | Historia | Flujo | Tiempo | Tokens | Reuse | Gates | Notas |
|-------|-------|----------|-------|--------|--------|-------|-------|-------|
| 2026-08-01 | qa-reviewer | AUTH-TOKEN-REFRESH | A+P+B | ~12 | less paste; MCP tools | yes | G1–G3 | Runbook IDE más claro que few-shot |
