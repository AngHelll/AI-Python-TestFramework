#!/usr/bin/env python3
"""Read-only synthetic / unified-diff reviewer (Phase 6 / P1).

Observes only — never writes fixes.

Usage:
  python3 scripts/review_diff.py --fixture uc05
  python3 scripts/review_diff.py --path knowledge/examples/review/uc06-thread-sleep.diff --json
  python3 scripts/review_diff.py eval
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REVIEW_ROOT = ROOT / "knowledge/examples/review"
FIXTURES = REVIEW_ROOT / "fixtures.json"
ALLOWLIST_PREFIXES = (
    "knowledge/examples/review/",
    "labs/csharp-reqnroll-lab/",
    "features/",
    "pages/",
    "tests/",
)

KNOWN_LOGIN_BUILDERS = {"LoginRequestBuilder"}
DUP_BUILDER_RE = re.compile(r"\bclass\s+(Login(?:Payload|Request)?Builder\d*|AuthLogin\w*Builder)\b")
SLEEP_CS_RE = re.compile(r"Thread\.Sleep\s*\(")
SLEEP_PY_RE = re.compile(r"\btime\.sleep\s*\(")
SECRET_RE = re.compile(
    r"""(api[_-]?key|secret|password)\s*=\s*['\"](?!valid_password|wrong_password)[^'\"]+['\"]""",
    re.I,
)
FEATURE_TAG_RE = re.compile(r"@(AUTH-[\w-]+|USER-[\w-]+|TEST_[\w-]+|smoke|login|negative|security|planned)\b")
SCENARIO_RE = re.compile(r"^\s*Scenario(?: Outline)?:\s*(.+)$")


def resolve_allowlisted(rel: str) -> Path:
    rel = rel.replace("\\", "/").lstrip("./")
    if not any(rel.startswith(p) for p in ALLOWLIST_PREFIXES):
        raise ValueError(f"Path not allowlisted for review: {rel}")
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    return path


def load_fixture_map() -> dict[str, dict[str, Any]]:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return {f["id"]: f for f in data["fixtures"]}


def added_lines(diff_text: str) -> list[tuple[str, int, str]]:
    """Return (path, line_no_in_new_file_approx, content) for added lines."""
    results: list[tuple[str, int, str]] = []
    current_path = ""
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            current_path = raw[6:].strip()
            new_line = 0
            continue
        if raw.startswith("@@"):
            # @@ -a,b +c,d @@
            m = re.search(r"\+(\d+)", raw)
            new_line = int(m.group(1)) - 1 if m else 0
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            new_line += 1
            results.append((current_path, new_line, raw[1:]))
        elif raw.startswith("-") and not raw.startswith("---"):
            continue
        elif raw.startswith(" "):
            new_line += 1
    return results


def review_text(diff_text: str, source_path: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    added = added_lines(diff_text)

    # Track scenario tags in added feature content
    pending_tags: list[str] = []
    for path, line, content in added:
        # Duplication builders
        for match in DUP_BUILDER_RE.finditer(content):
            name = match.group(1)
            if name not in KNOWN_LOGIN_BUILDERS:
                findings.append(
                    {
                        "code": "DUP-BUILDER",
                        "category": "duplication",
                        "severity": "high",
                        "path": path or source_path,
                        "line": line,
                        "message": (
                            f"New builder {name} looks like a duplicate of catalog "
                            f"{sorted(KNOWN_LOGIN_BUILDERS)}; prefer LoginRequestBuilder."
                        ),
                        "snippet": content.strip()[:120],
                    }
                )

        if SLEEP_CS_RE.search(content):
            findings.append(
                {
                    "code": "STAB-SLEEP-CS",
                    "category": "stability",
                    "severity": "high",
                    "path": path or source_path,
                    "line": line,
                    "message": "Thread.Sleep is forbidden on automation paths (AP-03).",
                    "snippet": content.strip()[:120],
                }
            )

        if SLEEP_PY_RE.search(content):
            findings.append(
                {
                    "code": "STAB-SLEEP-PY",
                    "category": "stability",
                    "severity": "high",
                    "path": path or source_path,
                    "line": line,
                    "message": "time.sleep is forbidden on automation paths (AP-03).",
                    "snippet": content.strip()[:120],
                }
            )

        if SECRET_RE.search(content):
            findings.append(
                {
                    "code": "SEC-SECRET",
                    "category": "security",
                    "severity": "high",
                    "path": path or source_path,
                    "line": line,
                    "message": "Possible hard-coded secret/password literal (AP-05).",
                    "snippet": content.strip()[:120],
                }
            )

        # XRay-like tags for feature diffs
        if path.endswith(".feature") or ".feature" in (path or source_path):
            stripped = content.strip()
            if stripped.startswith("@"):
                pending_tags.extend(re.findall(r"@([\w-]+)", stripped))
            elif SCENARIO_RE.match(content):
                tag_blob = " ".join(pending_tags)
                has_story = bool(re.search(r"(?:^|\s)(AUTH-|USER-|TEST_)", tag_blob)) or bool(
                    re.search(r"(AUTH-[\w-]+|USER-[\w-]+|TEST_[\w-]+)", tag_blob)
                )
                if not has_story:
                    title = SCENARIO_RE.match(content).group(1).strip()
                    findings.append(
                        {
                            "code": "XRAY-MISSING-TAG",
                            "category": "xray",
                            "severity": "medium",
                            "path": path or source_path,
                            "line": line,
                            "message": (
                                f"Scenario '{title}' lacks @AUTH-*/@USER-*/@TEST_* story tag."
                            ),
                            "snippet": content.strip()[:120],
                        }
                    )
                pending_tags = []
            elif stripped.startswith(("Given ", "When ", "Then ", "And ", "But ", "Background:")):
                pending_tags = []

    return findings


def review_path(rel: str) -> dict[str, Any]:
    path = resolve_allowlisted(rel)
    text = path.read_text(encoding="utf-8")
    findings = review_text(text, rel)
    return {
        "source": rel,
        "finding_count": len(findings),
        "findings": findings,
        "codes": sorted({f["code"] for f in findings}),
    }


def review_fixture(fixture_id: str, category: str | None = None) -> dict[str, Any]:
    fixtures = load_fixture_map()
    if fixture_id not in fixtures:
        raise KeyError(f"Unknown fixture {fixture_id}; known={sorted(fixtures)}")
    fx = fixtures[fixture_id]
    result = review_path(fx["path"])
    if category:
        result["findings"] = [f for f in result["findings"] if f.get("category") == category]
        result["codes"] = sorted({f["code"] for f in result["findings"]})
        result["finding_count"] = len(result["findings"])
    result["fixture_id"] = fixture_id
    result["uc"] = fx["uc"]
    result["category_filter"] = category
    result["expected_codes"] = fx["expected_codes"]
    # When filtering by category, only require expected codes that belong to that category's hit set
    expected = fx["expected_codes"]
    result["pass"] = all(code in result["codes"] for code in expected)
    return result


def cmd_eval(category: str | None = None) -> int:
    fixtures = load_fixture_map()
    results = []
    passed = 0
    for fid, fx in fixtures.items():
        if category and fx.get("category") != category:
            continue
        r = review_fixture(fid, category=None)
        results.append(r)
        if r["pass"]:
            passed += 1
        status = "PASS" if r["pass"] else "FAIL"
        print(f"- [{status}] {fid} ({r['uc']}) codes={r['codes']} expected={r['expected_codes']}")
    total = len(results)
    print(f"# reviewer eval {passed}/{total}" + (f" category={category}" if category else ""))
    out = ROOT / "docs/ai-evolution/evals/reviewer-baseline.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"passed": passed, "total": total, "category": category, "cases": results}, indent=2), encoding="utf-8")
    return 0 if passed == total and total > 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", help="Fixture id from fixtures.json")
    parser.add_argument("--path", help="Allowlisted relative path to a .diff/.feature/.cs")
    parser.add_argument(
        "--category",
        choices=["duplication", "stability", "xray", "security", "architecture"],
        help="Optional finding category filter / sub-reviewer lens",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("command", nargs="?", choices=["eval"], help="Run all fixtures")
    args = parser.parse_args()

    try:
        if args.command == "eval":
            return cmd_eval(category=args.category)
        if args.fixture:
            result = review_fixture(args.fixture, category=args.category)
        elif args.path:
            result = review_path(args.path)
            if args.category:
                result["findings"] = [f for f in result["findings"] if f.get("category") == args.category]
                result["codes"] = sorted({f["code"] for f in result["findings"]})
                result["finding_count"] = len(result["findings"])
        else:
            parser.error("Provide --fixture, --path, or eval")
            return 2
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"# review source={result.get('source')} findings={result['finding_count']}")
        for f in result["findings"]:
            print(f"- [{f['severity']}] {f['code']} {f['path']}:{f['line']} — {f['message']}")
        if "pass" in result:
            print(f"# fixture_pass={result['pass']}")
    return 0 if result.get("pass", True) else 1


if __name__ == "__main__":
    sys.exit(main())
