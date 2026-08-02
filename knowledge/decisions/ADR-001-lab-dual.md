# ADR-001: Laboratorio dual Python + C#

## Estado

Aceptado — 2026-07-30

## Contexto

El framework laboral es C# / Reqnroll / xUnit. Este repo es Python y ya tiene superficie de IA (prompts, agents, ForgeOne). El roadmap exige Context First y evals transferibles al stack laboral.

## Decisión

1. Mantener este repo como **plataforma / dogfood** de la práctica de IA.
2. Añadir `labs/csharp-reqnroll-lab` como **sujeto** reducido tipo trabajo.
3. No clonar el monorepo laboral.

## Consecuencias

- Hay que mantener mapeo de patrones y catálogo de componentes.
- Las evals golden deben correr contra el lab C# (y opcionalmente Python).
- La orquestación puede prototiparse en Python/Cursor antes de Semantic Kernel.
