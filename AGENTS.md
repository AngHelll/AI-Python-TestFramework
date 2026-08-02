# AGENTS.md — AI-Python-TestFramework

Primary guidance for AI assistants working in this **Python Selenium / Pytest / Behave** automation framework.

## Mission

Help generate and debug tests that follow **Page Object Model**, dual Pytest + Behave approaches, and the context under `prompts/`.

## Prefer

- Inherit page objects from `BasePage`; use `LOCATORS` dicts
- Type hints, docstrings, logging, screenshots on failure
- Config via `.env` / `config/` — never commit secrets
- Least-privilege tools in Copilot agents (prefer `read` / `search` / `edit`)

## Surfaces

| Surface | Path |
|---------|------|
| Copilot agents | `.github/agents/` |
| Copilot prompts | `.github/prompts/` |
| Skills | `.github/skills/` |
| Framework AI context | `prompts/context/` |
| Knowledge base (roadmap) | `knowledge/` |
| AI evolution docs | `docs/ai-evolution/` |
| C# Reqnroll lab (work-stack twin) | `labs/csharp-reqnroll-lab/` |
| Cursor rules | `.cursor/rules/` |

## AI evolution (Analyst → Planner)

- **Fase 0–8:** `docs/ai-evolution/PHASE-*.md`
- **Portar a otro repo:** `docs/ai-evolution/PORTABLE-BLUEPRINT.md` + `docs/ai-evolution/bootstrap/`
- **Smokes:** `bash scripts/run_all_smokes.sh`
- **Agent contracts:** `knowledge/agents/contracts.md`
- Agents: analyst, planner, builder, reviewer
- Lab: `labs/csharp-reqnroll-lab/`
- Credentials: copy `.env.example` → `.env` (gitignored); never commit API keys
