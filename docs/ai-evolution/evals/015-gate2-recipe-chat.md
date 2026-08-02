# Eval 015 — Gate2 recipe chat (allowlisted choose → propose)

**Fecha:** 2026-08-01  
**Command:** `python3 scripts/gate2_recipe_chat.py smoke`  
**Contract:** `gate2-recipe-choice.v1`  
**Baseline:** [gate2-recipe-chat-baseline.json](gate2-recipe-chat-baseline.json)

## Objetivo

Tras Gate 2, elegir una **recipe allowlisted** (o skip si `already_covered`) y opcionalmente `propose` — **nunca apply**.

## Criterios smoke

| Check | Esperado |
|-------|----------|
| recipes_align_registry | ids = propose_patch enum |
| skip_already_covered | AUTH-DUPLICATE-BUILDER → skip |
| choose_access_token_recipe | → `good-access-token-expired` |
| propose_awaiting_gate3 | status awaiting_gate3, clean |
| choose_refresh_recipe | → `good-refresh-token-expired` |
| llm_optional | SKIP sin key / PASS con key |
| no_apply_in_chooser | solo propose |

## Uso

```bash
python3 scripts/gate2_recipe_chat.py choose \
  --request-id AUTH-TOKEN-REFRESH --terms "access token" --propose

# Opcional LLM
OPENAI_API_KEY=… python3 scripts/gate2_recipe_chat.py choose \
  --request-id AUTH-TOKEN-REFRESH --terms "access token" --llm --propose
```

## Resultado

| Check | Status |
|-------|--------|
| smoke | **7/7 PASS** |
| En `run_all_smokes.sh` | Sí |
| Host .NET | `recipe-smoke` / `recipe-chat` |
