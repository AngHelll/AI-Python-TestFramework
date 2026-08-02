---
agent: automation-planner
---

# Plan automation request

**Request ID:** ${input:request_id}  
**Target:** ${input:target}  
**Domain:** ${input:domain}

## Approved analysis (paste)

${input:analysis}

## Description

${input:description}

## Required behavior

1. Load context per `prompts/fragments/context-load-order.md`.
2. Apply fragments: anti-patterns, guardrails, gate-criteria (Gate 2).
3. **Search via tools registry only:**
   `python3 scripts/tools_runner.py invoke find_existing_builder --arg target=… --arg terms=…`
4. Emit output matching **`prompts/contracts/plan.v1.yaml`** (YAML fenced block).
5. No patches. No full source files.
6. If analysis marked already covered → empty `create_only_if_needed` and high risk on duplication.
7. Login payload construction in C# lab → must reuse `LoginRequestBuilder` (see approved FS-03).

Approved few-shots: `prompts/examples/approved/`.  
Registry: `tools/registry/v1/README.md`.
