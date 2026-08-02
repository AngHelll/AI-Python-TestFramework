#!/usr/bin/env bash
# Run all AI-evolution regression smokes (Phases 4–7).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> retrieval eval @5"
python3 scripts/eval_retrieval.py --k 5

echo "==> tools_runner smoke"
python3 scripts/tools_runner.py smoke

echo "==> workflow_runner smoke"
python3 scripts/workflow_runner.py smoke

echo "==> review_diff eval"
python3 scripts/review_diff.py eval

echo "==> patch_pipeline smoke"
python3 scripts/patch_pipeline.py smoke

echo "==> gate_timing smoke"
python3 scripts/gate_timing.py smoke

echo "==> mcp_lab smoke"
python3 scripts/mcp_lab_smoke.py

echo "==> gate2_recipe_chat smoke"
python3 scripts/gate2_recipe_chat.py smoke

echo "==> all AI evolution smokes passed"
