#!/usr/bin/env python3
"""Read-only helper: find Builders / Validators / Steps / Features / knowledge by query.

Usage:
  python3 scripts/find_existing_components.py --target csharp --query login
  python3 scripts/find_existing_components.py --target knowledge --query sleep
  python3 scripts/find_existing_components.py --target csharp --terms RefreshToken,refresh --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEARCH_ROOTS: dict[str, dict[str, Path]] = {
    "csharp": {
        "builders": ROOT / "labs/csharp-reqnroll-lab/src/AutomationLab/Builders",
        "validators": ROOT / "labs/csharp-reqnroll-lab/src/AutomationLab/Validators",
        "clients": ROOT / "labs/csharp-reqnroll-lab/src/AutomationLab/Clients",
        "pages": ROOT / "labs/csharp-reqnroll-lab/src/AutomationLab/Pages",
        "steps": ROOT / "labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Steps",
        "features": ROOT / "labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Features",
        "support": ROOT / "labs/csharp-reqnroll-lab/tests/AutomationLab.Tests/Support",
    },
    "python": {
        "pages": ROOT / "pages",
        "steps": ROOT / "features/steps",
        "features": ROOT / "features",
        "utils": ROOT / "utils",
    },
    "knowledge": {
        "knowledge": ROOT / "knowledge",
        "fragments": ROOT / "prompts/fragments",
        "contracts": ROOT / "prompts/contracts",
        "approved_examples": ROOT / "prompts/examples/approved",
    },
}

SYMBOL_PATTERNS = [
    re.compile(r"\b(?:class|interface|static class)\s+(\w+)"),
    re.compile(r"^\s*Feature:\s*(.+)$", re.MULTILINE),
    re.compile(r"@(AUTH-[\w-]+|USER-[\w-]+|smoke|login|negative|planned)"),
]

CODE_SUFFIXES = {".cs", ".feature", ".py", ".md", ".yaml", ".yml", ".json"}


def iter_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(
        p
        for p in directory.rglob("*")
        if p.is_file()
        and p.suffix in CODE_SUFFIXES
        and ".feature.cs" not in p.name
    )


def term_score(text: str, name: str, rel_path: str, terms: list[str]) -> int:
    blob = f"{name}\n{rel_path}\n{text}"
    blob_l = blob.lower()
    score = 0
    for term in terms:
        t = term.lower()
        if t in blob_l:
            score += 1
        if t in name.lower() or t in rel_path.lower():
            score += 2
        # Prefer whole-identifier matches (RefreshToken vs RefreshTokenData)
        if re.search(rf"\b{re.escape(term)}\b", blob, flags=re.IGNORECASE):
            score += 3
    return score


def scan(
    target: str,
    terms: list[str],
    limit: int | None = None,
    kinds: list[str] | None = None,
) -> list[dict[str, object]]:
    if not terms:
        return []

    roots = SEARCH_ROOTS[target]
    allowed_kinds = set(kinds) if kinds else None
    hits: list[dict[str, object]] = []

    for kind, directory in roots.items():
        if allowed_kinds is not None and kind not in allowed_kinds:
            continue
        for path in iter_files(directory):
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = path.relative_to(ROOT).as_posix()
            score = term_score(text, path.name, rel, terms)
            if score <= 0:
                continue
            symbols: list[str] = []
            for pattern in SYMBOL_PATTERNS:
                for match in pattern.finditer(text):
                    symbols.append(match.group(0).strip())
            hits.append(
                {
                    "kind": kind,
                    "path": rel,
                    "score": score,
                    "symbols": ", ".join(list(dict.fromkeys(symbols))[:8]) if symbols else path.stem,
                }
            )

    hits.sort(key=lambda h: (-int(h["score"]), str(h["path"])))
    if limit is not None:
        hits = hits[:limit]
    return hits


def resolve_terms(query: str | None, terms_arg: str | None) -> list[str]:
    if terms_arg:
        return [t.strip() for t in terms_arg.split(",") if t.strip()]
    if query:
        # Prefer whole query plus tokenized words (length > 2)
        tokens = [query] + [t for t in re.split(r"\s+", query.strip()) if len(t) > 2]
        # Dedupe preserving order
        return list(dict.fromkeys(tokens))
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=sorted(SEARCH_ROOTS), required=True)
    parser.add_argument("--query", help="Free-text query (tokenized if --terms omitted)")
    parser.add_argument("--terms", help="Comma-separated explicit terms (recommended for evals)")
    parser.add_argument("--json", action="store_true", help="Emit JSON array of hits")
    parser.add_argument("--limit", type=int, default=None, help="Max hits after ranking")
    args = parser.parse_args()

    terms = resolve_terms(args.query, args.terms)
    if not terms:
        parser.error("Provide --query and/or --terms")

    hits = scan(args.target, terms, limit=args.limit)
    if args.json:
        print(json.dumps(hits, indent=2))
        return 0 if hits else 1

    if not hits:
        print(f"No matches for terms={terms!r} target={args.target}")
        return 1

    joined = args.query or args.terms
    print(f"# find_existing_components target={args.target} query={joined!r} terms={terms!r}")
    for hit in hits:
        print(f"- [{hit['kind']}] score={hit['score']} {hit['path']}")
        print(f"  symbols: {hit['symbols']}")
    print(f"\n# total: {len(hits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
