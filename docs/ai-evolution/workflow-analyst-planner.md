# Workflow — Análisis y planificación asistida

**Versión:** 0.1  
**Madurez objetivo:** Nivel 5 (workflow determinista) sin escritura de código  
**Caso de uso primario:** UC-01 … UC-04

## 1. Propósito

Dada una solicitud de nueva automatización (o extensión), producir un **análisis funcional** y un **plan técnico** trazable, con evidencia del repositorio, sin modificar archivos.

## 2. Roles

| Rol | Responsabilidad | No hace |
|-----|-----------------|---------|
| **Analyst** | Resumen funcional, cobertura, escenarios +/-, bordes, dudas | Código, plan de archivos |
| **Planner** | Reutilización, archivos afectados, riesgos técnicos, plan ordenado | Código, merge |
| **Human** | Gate 1 (análisis) y Gate 2 (plan) | — |
| **Orquestador** | Estado, orden, tracing, adjuntar evidencia | Decidir arquitectura solo |

## 3. Entradas

| Campo | Obligatorio | Ejemplo |
|-------|-------------|---------|
| `request_id` | Sí | `AUTH-TOKEN-REFRESH` |
| `description` | Sí | Texto de historia / aceptación |
| `domain` | Sí | `Auth` |
| `target` | Sí | `labs/csharp-reqnroll-lab` \| `python-root` |
| `constraints` | No | “No UI”, “solo API” |
| `jira_id` | No | Stub hasta integración real |
| `xray_key` | No | Stub |

## 4. Fuentes de contexto (orden de consulta)

1. `knowledge/` (architecture, patterns, anti-patterns, bdd, mapping).
2. Catálogo de componentes del target (`Builders/`, `Validators/`, `Steps/`, `pages/` / `Pages/`).
3. Features y tests similares (búsqueda por dominio / tags).
4. Ejemplos canónicos en `knowledge/examples/`.
5. Decisiones (`knowledge/decisions/`) y known-issues.
6. (Futuro) Jira / XRay vía tools read-only.

Toda salida debe listar **evidencia consultada** (paths + por qué).

## 5. Flujo

```text
Solicitud
   ↓
Recuperar contexto (target + knowledge)
   ↓
Analyst → Análisis funcional
   ↓
[Human Gate 1 — Análisis]
   ↓
Buscar automatizaciones similares + componentes reutilizables
   ↓
Planner → Plan técnico
   ↓
[Human Gate 2 — Plan]
   ↓
Entrega (artefacto versionable) — SIN patch
```

## 6. Salidas estructuradas

### 6.1 Análisis funcional (`analysis`)

```yaml
request_id: string
summary: string
proposed_coverage:
  positive: [string]
  negative: [string]
  edge: [string]
assumptions: [string]
open_questions: [string]
out_of_scope: [string]
evidence: [{ path: string, reason: string }]
```

### 6.2 Plan técnico (`plan`)

```yaml
request_id: string
reuse:
  builders: [string]
  validators: [string]
  steps: [string]
  pages_or_clients: [string]
create_only_if_needed: [string]  # justificar cada uno
files_likely_affected: [string]
risks: [{ id: string, severity: low|medium|high, note: string }]
implementation_steps: [string]  # ordenados, sin código completo
evidence: [{ path: string, reason: string }]
policy_checks:
  searched_before_create: bool
  no_critical_files_without_flag: bool
```

## 7. Human gates

### Gate 1 — Análisis

Aprobar si: cobertura razonable, supuestos explícitos, dudas listadas, sin inventar requisitos.

### Gate 2 — Plan

Aprobar si: se buscó reutilización, cada “crear nuevo” está justificado, riesgos y archivos son creíbles.

Rechazo → volver a Analyst o Planner con motivo (trazado en estado).

## 8. Herramientas (Fase 4/5 — contratos)

Solo lectura en esta fase:

| Tool | Propósito |
|------|-----------|
| `search_similar_automation` | Features/tests parecidos |
| `find_existing_builder` | Builders por nombre/dominio |
| `find_existing_validator` | Validators |
| `find_reusable_step` | Steps Reqnroll/Behave |
| `inspect_service_contract` | Modelos / clientes API |
| `validate_naming` | Convenciones |
| `detect_forbidden_patterns` | Sleeps, secrets patterns (en código existente) |
| `get_changed_files` | Si hay rama de trabajo |

Implementación: **Phase 4** — `python3 scripts/tools_runner.py` + `tools/registry/v1/registry.json` (read-only, audited).  
Jira/XRay siguen como stubs (sin red).

## 9. Políticas aplicables

Ver roadmap §9 y `knowledge/review-checklists/guardrails.md`.

Mínimo obligatorio en este workflow:

- No proponer crear Builder/Validator/Step sin búsqueda documentada.
- No presentar inferencias como hechos de código.
- No omitir evidencia.
- No generar parches en esta fase.

## 10. Métricas del workflow

- % planes con ≥1 componente reutilizado correctamente.
- % omisiones de builder existente (golden AUTH-DUPLICATE-BUILDER).
- Correcciones humanas Gate 1 / Gate 2.
- Tiempo Analyst + Planner vs few-shot baseline.
- Contexto irrelevante incluido (ruido de retrieval).

## 11. Tracing mínimo

Cada ejecución guarda:

```json
{
  "run_id": "...",
  "request_id": "...",
  "target": "...",
  "stages": ["context", "analysis", "gate1", "plan", "gate2"],
  "tools_invoked": [],
  "evidence": [],
  "gate1": "pending|approved|rejected",
  "gate2": "pending|approved|rejected",
  "model": "...",
  "timestamp": "..."
}
```

Ubicación: `.forgeone/runs/workflow/` (live, gitignored) y goldens en `docs/ai-evolution/evals/runs/`.  
Orquestador: `python3 scripts/workflow_runner.py` (Fase 5).

## 12. Criterio de “hecho” para v1

- Contratos de salida estables (arriba).
- Al menos 3 historias del golden set con análisis+plan y Gate humano simulado.
- AUTH-DUPLICATE-BUILDER falla el few-shot “ingenuo” y pasa el workflow (encuentra builder existente).
