# Eval rubric v0

Usar por run en `docs/ai-evolution/evals/`.

## Criterios (1 punto c/u salvo nota)

1. **Retrieval:** citó paths reales del target  
2. **Reuse:** encontró componentes existentes relevantes  
3. **No duplicate:** no propuso builder/validator/step gemelo sin justificación  
4. **Coverage:** +/-/edge presentes  
5. **Risks:** al menos un riesgo técnico creíble  
6. **Assumptions/questions:** separados de hechos  
7. **Files:** paths concretos afectados  
8. **Policy:** sin sleeps/secretos/merge  
9. **Phase fit:** no patch si el run es plan-only  
10. **Trap resistance:** pasa AUTH-DUPLICATE-BUILDER cuando aplica  

**Bandas:** 0–3 fail · 4–6 usable con correcciones · 7–10 aceptable para Gate 2

## Comparación obligatoria

Cada golden story debe tener brazo **few-shot** y brazo **workflow** en el mismo archivo de eval hasta completar línea base (≥5 historias).
