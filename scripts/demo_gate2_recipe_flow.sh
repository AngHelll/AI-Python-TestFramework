#!/usr/bin/env bash
# End-to-end demo: plan context → Gate2 recipe choose → propose (no apply).
# Usage: bash scripts/demo_gate2_recipe_flow.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> 1) already_covered → skip propose"
python3 scripts/gate2_recipe_chat.py choose \
  --request-id AUTH-DUPLICATE-BUILDER \
  --terms LoginRequestBuilder \
  --propose --json | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['action']=='skip', d; print('OK skip', d['reason'][:70])"

echo "==> 2) token refresh → choose + propose awaiting_gate3"
python3 scripts/gate2_recipe_chat.py choose \
  --request-id AUTH-TOKEN-REFRESH \
  --terms "access token expired" \
  --propose --json | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['action']=='propose', d; assert d['recipe_id']=='good-access-token-expired', d; assert d['proposal']['status']=='awaiting_gate3', d; print('OK propose', d['proposal']['proposal_id'])"

echo "==> 3) refresh wording → good-refresh-token-expired (choose only)"
python3 scripts/gate2_recipe_chat.py choose \
  --request-id PATCH-REFRESH \
  --terms "refresh token expired" \
  --json | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['recipe_id']=='good-refresh-token-expired', d; print('OK recipe', d['recipe_id'])"

echo "==> demo_gate2_recipe_flow PASS (no apply)"
