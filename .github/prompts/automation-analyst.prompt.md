---
agent: automation-analyst
---

# Analyze automation request

**Request ID:** ${input:request_id}  
**Target:** ${input:target}  
**Domain:** ${input:domain}

## Description

${input:description}

## Constraints

${input:constraints}

## Required behavior

1. Load context per `prompts/fragments/context-load-order.md`.
2. Apply `prompts/fragments/anti-patterns.md` and `prompts/fragments/guardrails.md`.
3. Emit output matching **`prompts/contracts/analysis.v1.yaml`** (YAML fenced block).
4. Read-only. No code. No patches.
5. If coverage already exists, set `meta.already_covered: true` and keep create lists empty in spirit (Analyst does not plan files — state already covered in summary).

Gate criteria: `prompts/fragments/gate-criteria.md` (Gate 1).
