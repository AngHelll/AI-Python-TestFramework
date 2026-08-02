#!/usr/bin/env bash
# Guided human gate-timing sessions (interactive stopwatch).
# Usage: bash scripts/run_human_sessions.sh [reviewer_name]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
REVIEWER="${1:-qa-reviewer}"

echo "==> Human gate sessions for reviewer=$REVIEWER"
echo "    Have a stopwatch ready. Durations: 90 / 90s / 1:30 / 2m"
echo

python3 scripts/gate_timing.py human --scenario duplicate --interactive --reviewer "$REVIEWER" --note "pair interactive"
echo
python3 scripts/gate_timing.py human --scenario token-refresh --interactive --reviewer "$REVIEWER" --note "pair interactive"
echo
python3 scripts/gate_timing.py human --scenario login-neg --interactive --reviewer "$REVIEWER" --note "pair interactive"
echo
python3 scripts/gate_timing.py summarize
echo
echo "==> Logs under docs/ai-evolution/evals/human-sessions/"
ls -1 docs/ai-evolution/evals/human-sessions/*.md 2>/dev/null | tail -5 || true
