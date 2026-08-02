#!/usr/bin/env python3
"""Evaluate retrieval recall against knowledge/examples/retrieval-seeds.json.

Metrics per case:
  - hit_at_k: expected path appears in top-k ranked results (default k=5)
  - noise: number of returned paths that are not in expected_paths (informational)

Usage:
  python3 scripts/eval_retrieval.py
  python3 scripts/eval_retrieval.py --k 3 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from find_existing_components import scan  # noqa: E402

SEEDS = ROOT / "knowledge/examples/retrieval-seeds.json"


def evaluate(k: int) -> dict:
    data = json.loads(SEEDS.read_text(encoding="utf-8"))
    results = []
    passed = 0

    for case in data["cases"]:
        terms = case["terms"]
        target = case["target"]
        expected = case["expected_paths"]
        hits = scan(target, terms, limit=k)
        hit_paths = [h["path"] for h in hits]
        found = [p for p in expected if p in hit_paths]
        missing = [p for p in expected if p not in hit_paths]
        noise = [p for p in hit_paths if p not in expected]
        ok = len(missing) == 0
        if ok:
            passed += 1
        results.append(
            {
                "id": case["id"],
                "query": case["query"],
                "target": target,
                "terms": terms,
                "pass": ok,
                "found": found,
                "missing": missing,
                "top_k_paths": hit_paths,
                "noise_count": len(noise),
                "noise_sample": noise[:5],
                "eval_ref": case.get("eval_ref"),
            }
        )

    total = len(results)
    return {
        "seeds_version": data.get("version"),
        "k": k,
        "passed": passed,
        "total": total,
        "recall_at_k": round(passed / total, 3) if total else 0.0,
        "cases": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=5, help="Recall@k window")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = evaluate(args.k)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"# retrieval eval seeds={report['seeds_version']} k={report['k']}")
        print(f"# recall@{report['k']}: {report['passed']}/{report['total']} = {report['recall_at_k']}")
        print()
        for case in report["cases"]:
            status = "PASS" if case["pass"] else "FAIL"
            print(f"- [{status}] {case['id']} ({case['query']})")
            if case["missing"]:
                print(f"  missing: {case['missing']}")
            print(f"  top-{args.k}: {case['top_k_paths']}")
            print(f"  noise_count: {case['noise_count']}")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
