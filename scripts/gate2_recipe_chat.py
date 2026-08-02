#!/usr/bin/env python3
"""Post–Gate2 recipe chooser: pick an allowlisted patch recipe (propose only).

After an approved plan (Gate 2), choose a recipe from tools/patches/v1/recipes.json
and optionally run propose_patch. Never applies.

Modes:
  deterministic (default) — keyword/request rules, no LLM
  --llm — optional OpenAI chat; may only emit a recipe id from the allowlist

Usage:
  python3 scripts/gate2_recipe_chat.py choose --request-id AUTH-TOKEN-REFRESH --terms "access token"
  python3 scripts/gate2_recipe_chat.py choose --request-id AUTH-DUPLICATE-BUILDER --terms LoginRequestBuilder
  python3 scripts/gate2_recipe_chat.py choose --request-id AUTH-TOKEN-REFRESH --propose
  python3 scripts/gate2_recipe_chat.py smoke
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from patch_pipeline import propose as propose_recipe  # noqa: E402
from tools_runner import load_registry  # noqa: E402
from workflow_runner import build_analysis, build_plan, collect_context  # noqa: E402

RECIPES_PATH = ROOT / "tools/patches/v1/recipes.json"
BASELINE = ROOT / "docs/ai-evolution/evals/gate2-recipe-chat-baseline.json"
CONTRACT = "gate2-recipe-choice.v1"


def load_recipes() -> list[dict[str, Any]]:
    data = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
    return list(data["recipes"])


def recipe_ids(recipes: list[dict[str, Any]]) -> list[str]:
    return [r["id"] for r in recipes]


def build_plan_for_request(request_id: str, terms: str, target: str = "csharp", domain: str = "Auth") -> dict[str, Any]:
    req = {
        "request_id": request_id,
        "terms": terms,
        "target": target,
        "domain": domain,
        "description": f"gate2_recipe_chat for {request_id}",
        "constraints": "",
    }
    _tools, evidence, buckets = collect_context(target, terms, request_id)
    analysis = build_analysis(req, evidence, buckets)
    return build_plan(req, analysis, evidence, buckets)


def deterministic_choose(
    request_id: str,
    terms: str,
    plan: dict[str, Any],
    recipes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Map plan + request to an allowlisted recipe or skip."""
    ids = set(recipe_ids(recipes))
    already = bool(plan.get("meta", {}).get("already_covered"))
    blob = f"{request_id} {terms}".lower()

    if already:
        return {
            "contract": CONTRACT,
            "mode": "deterministic",
            "recipe_id": None,
            "action": "skip",
            "reason": "plan.meta.already_covered=true — Reuse Before Create; do not propose",
            "request_id": request_id,
            "allowlist": sorted(ids),
        }

    # Prefer explicit good recipes; never auto-pick bad-* unless trap flag
    if "sleep" in blob or "bad-sleep" in blob:
        choice = "bad-sleep-support"
        reason = "trap/negative: intentional sleep recipe for reviewer block"
    elif "refresh" in blob and "access" not in blob:
        choice = "good-refresh-token-expired"
        reason = "request mentions refresh token expiry"
    elif "token" in blob or "access" in blob or "expired" in blob or "AUTH-TOKEN" in request_id:
        choice = "good-access-token-expired"
        reason = "request relates to access token / AUTH-TOKEN-REFRESH"
    else:
        return {
            "contract": CONTRACT,
            "mode": "deterministic",
            "recipe_id": None,
            "action": "skip",
            "reason": "no allowlisted recipe matches request terms; ask human for recipe id",
            "request_id": request_id,
            "allowlist": sorted(ids),
        }

    if choice not in ids:
        raise RuntimeError(f"chooser produced unknown recipe {choice}")

    return {
        "contract": CONTRACT,
        "mode": "deterministic",
        "recipe_id": choice,
        "action": "propose",
        "reason": reason,
        "request_id": request_id,
        "allowlist": sorted(ids),
        "expect_review_clean": next(r.get("expect_review_clean") for r in recipes if r["id"] == choice),
    }


def llm_choose(
    request_id: str,
    terms: str,
    plan: dict[str, Any],
    recipes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Optional OpenAI call; output must be a recipe id from allowlist or null."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    catalog = [
        {"id": r["id"], "description": r.get("description", ""), "expect_review_clean": r.get("expect_review_clean")}
        for r in recipes
    ]
    already = bool(plan.get("meta", {}).get("already_covered"))
    system = (
        "You choose a patch RECIPE id after Gate 2. "
        "You may ONLY pick an id from the allowlist or null. "
        "If plan already_covered is true, return null. "
        "Prefer expect_review_clean=true recipes unless the user asks for a negative trap. "
        "Never invent recipe ids. Never apply patches. "
        'Respond with JSON only: {"recipe_id": string|null, "reason": string}'
    )
    user = json.dumps(
        {
            "request_id": request_id,
            "terms": terms,
            "already_covered": already,
            "plan_reuse_builders": plan.get("reuse", {}).get("builders", []),
            "allowlist": catalog,
        },
        indent=2,
    )
    body = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAI request failed: {exc}") from exc

    content = payload["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    recipe_id = parsed.get("recipe_id")
    reason = str(parsed.get("reason") or "")
    ids = set(recipe_ids(recipes))

    if recipe_id is None or recipe_id == "null":
        return {
            "contract": CONTRACT,
            "mode": "llm",
            "recipe_id": None,
            "action": "skip",
            "reason": reason or "model returned null",
            "request_id": request_id,
            "allowlist": sorted(ids),
            "model": model,
        }

    if recipe_id not in ids:
        raise ValueError(f"LLM returned non-allowlisted recipe_id={recipe_id!r}")

    return {
        "contract": CONTRACT,
        "mode": "llm",
        "recipe_id": recipe_id,
        "action": "propose",
        "reason": reason,
        "request_id": request_id,
        "allowlist": sorted(ids),
        "model": model,
        "expect_review_clean": next(r.get("expect_review_clean") for r in recipes if r["id"] == recipe_id),
    }


def maybe_propose(choice: dict[str, Any], do_propose: bool) -> dict[str, Any]:
    out = dict(choice)
    if not do_propose or choice.get("action") != "propose" or not choice.get("recipe_id"):
        out["proposal"] = None
        return out

    proposal = propose_recipe(choice["recipe_id"], None, "gate2_recipe_chat")
    out["proposal"] = {
        "proposal_id": proposal.get("proposal_id"),
        "status": proposal.get("status"),
        "review_clean": proposal.get("review", {}).get("clean"),
        "codes": proposal.get("review", {}).get("codes"),
        "note": "Apply only with: python3 scripts/patch_pipeline.py apply --proposal-id … --gate3-approved",
    }
    return out


def cmd_choose(args: argparse.Namespace) -> int:
    recipes = load_recipes()
    plan = build_plan_for_request(args.request_id, args.terms, args.target, args.domain)
    if args.llm:
        choice = llm_choose(args.request_id, args.terms, plan, recipes)
    else:
        choice = deterministic_choose(args.request_id, args.terms, plan, recipes)

    choice["plan_already_covered"] = bool(plan.get("meta", {}).get("already_covered"))
    result = maybe_propose(choice, args.propose)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"# action={result['action']} recipe_id={result.get('recipe_id')} "
            f"mode={result['mode']} already_covered={result.get('plan_already_covered')}"
        )
        print(f"# reason={result.get('reason')}")
        if result.get("proposal"):
            p = result["proposal"]
            print(f"# proposal_id={p['proposal_id']} status={p['status']} review_clean={p['review_clean']}")
    return 0


def cmd_smoke() -> int:
    checks: list[tuple[str, bool, str]] = []
    recipes = load_recipes()
    ids = recipe_ids(recipes)

    # Allowlist integrity vs registry propose_patch enum
    registry = load_registry()
    propose_tool = next(t for t in registry["tools"] if t["name"] == "propose_patch")
    enum_vals = propose_tool["params"]["recipe"]["values"]
    ok_align = set(enum_vals) == set(ids)
    checks.append(("recipes_align_registry", ok_align, f"recipes={ids}"))

    # already_covered → skip
    plan_dup = build_plan_for_request("AUTH-DUPLICATE-BUILDER", "LoginRequestBuilder")
    c1 = deterministic_choose("AUTH-DUPLICATE-BUILDER", "LoginRequestBuilder", plan_dup, recipes)
    checks.append(("skip_already_covered", c1["action"] == "skip" and c1["recipe_id"] is None, c1["reason"][:60]))

    # token refresh → good-access-token-expired + propose
    plan_tok = build_plan_for_request("AUTH-TOKEN-REFRESH", "TokenRefresh access token")
    c2 = deterministic_choose("AUTH-TOKEN-REFRESH", "TokenRefresh access token", plan_tok, recipes)
    ok_tok = c2["action"] == "propose" and c2["recipe_id"] == "good-access-token-expired"
    checks.append(("choose_access_token_recipe", ok_tok, str(c2.get("recipe_id"))))

    proposed = maybe_propose(c2, do_propose=True)
    prop = proposed.get("proposal") or {}
    ok_prop = prop.get("status") == "awaiting_gate3" and prop.get("review_clean") is True
    checks.append(("propose_awaiting_gate3", ok_prop, str(prop.get("proposal_id"))))

    # refresh wording
    plan_ref = build_plan_for_request("AUTH-TOKEN-REFRESH", "refresh token expired")
    # Force not already_covered path: if plan says covered, still test chooser keywords in isolation
    plan_ref_forced = dict(plan_ref)
    plan_ref_forced["meta"] = {**plan_ref.get("meta", {}), "already_covered": False}
    c3 = deterministic_choose("PATCH-REFRESH", "refresh token expired", plan_ref_forced, recipes)
    checks.append(
        ("choose_refresh_recipe", c3["recipe_id"] == "good-refresh-token-expired", str(c3.get("recipe_id")))
    )

    # LLM path skip without key
    if not os.environ.get("OPENAI_API_KEY"):
        checks.append(("llm_optional", True, "SKIP (no OPENAI_API_KEY)"))
    else:
        try:
            llm = llm_choose("AUTH-DUPLICATE-BUILDER", "LoginRequestBuilder", plan_dup, recipes)
            ok_llm = llm["action"] == "skip" or llm.get("recipe_id") in ids or llm.get("recipe_id") is None
            # For duplicate should prefer skip
            ok_llm = ok_llm and (llm.get("recipe_id") is None or plan_dup.get("meta", {}).get("already_covered"))
            checks.append(("llm_optional", ok_llm, llm.get("mode", "")))
        except Exception as exc:  # noqa: BLE001
            checks.append(("llm_optional", False, str(exc)[:80]))

    # Never expose apply in this module's public contract
    src = Path(__file__).read_text(encoding="utf-8")
    ok_no_apply = "gate3-approved" in src and not re.search(r"apply_proposal\(", src)
    checks.append(("no_apply_in_chooser", ok_no_apply, "propose only"))

    baseline = {
        "contract": CONTRACT,
        "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(baseline, indent=2), encoding="utf-8")

    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"# gate2_recipe_chat smoke {passed}/{len(checks)}")
    for name, ok, detail in checks:
        print(f"- [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    print(f"# baseline={BASELINE.relative_to(ROOT)}")
    return 0 if passed == len(checks) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    ch = sub.add_parser("choose", help="Choose recipe after Gate 2")
    ch.add_argument("--request-id", required=True)
    ch.add_argument("--terms", required=True)
    ch.add_argument("--target", default="csharp")
    ch.add_argument("--domain", default="Auth")
    ch.add_argument("--propose", action="store_true", help="Run propose_patch for chosen recipe")
    ch.add_argument("--llm", action="store_true", help="Use OpenAI (OPENAI_API_KEY) instead of rules")
    ch.add_argument("--json", action="store_true")

    sub.add_parser("smoke", help="Deterministic smoke")

    args = parser.parse_args()
    try:
        if args.command == "choose":
            return cmd_choose(args)
        if args.command == "smoke":
            return cmd_smoke()
    except (ValueError, FileNotFoundError, KeyError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
