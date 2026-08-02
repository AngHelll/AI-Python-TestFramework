# Guardrails checklist (copiar a cada run)

- [ ] Se buscó Builder/Validator/Step existente (evidencia en salida).
- [ ] No se proponen secretos ni credenciales reales.
- [ ] No se proponen sleeps fijos.
- [ ] No se eliminan assertions.
- [ ] Inferencias marcadas como supuestos, no como hechos.
- [ ] Evidencia de paths consultados listada.
- [ ] Fase actual no genera patch si el workflow es solo análisis/plan.
- [ ] Target correcto (Python vs C# lab) según `request.target`.
- [ ] Historia trampa AUTH-DUPLICATE-BUILDER: debe reutilizar `LoginRequestBuilder`.
