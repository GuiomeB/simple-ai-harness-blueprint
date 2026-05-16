#!/usr/bin/env python3
"""check_pr_rail_consistency.py — fail PRs where the declared risk rail
mismatches the touched paths against .github/CODEOWNERS.

Rules:
  - `green` PR touching any path under .github/CODEOWNERS → FAIL with hint to
    reclassify to `amber` or `red`.
  - `amber` or `red` declarations: always pass (the rail-guard does not enforce
    upward classification; that's for human review).
  - PR without a `Rail:` line: FAIL with hint to add one.

Inputs (in order of preference):
  1. CLI flags: --pr-body PATH --changed-files PATH (local testing)
  2. Environment variables (GitHub Actions): PR_BODY, BASE_SHA, HEAD_SHA
  3. Falls back to `git diff origin/main...HEAD` if no env / flags given.

Exit codes:
  0 — pass
  1 — rail missing or mismatched (rejected PR)
  2 — internal error (missing CODEOWNERS, etc.)
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()

# Match a real rail declaration:
#   - Optional leading list marker / whitespace
#   - "Rail:" (case-insensitive)
#   - Optional markdown decoration (`, *, _) around the value
#   - The value: green | amber | red
#   - Optional closing decoration, then end-of-line (no trailing content)
# The end-of-line anchor is critical: it rejects the placeholder line
# "Rail: green | amber | red" (left in the template by an agent that didn't
# pick a value), because the trailing "| amber | red" prevents the match.
RAIL_RE = re.compile(
    r"^[\s\-*]*Rail:\s*[`*_]*(green|amber|red)[`*_]*\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def parse_codeowners(path: Path) -> list[str]:
    """Return CODEOWNERS path patterns (first column of each non-comment line).

    Normalizations applied:
      - leading `/` is stripped (CODEOWNERS treats `/src/**` as repo-relative;
        our matcher uses repo-relative paths already)
      - `!negation` patterns are silently skipped (full gitignore semantics is
        out of scope for this guard; a missed exception is preferable to a
        false negative on the rail)
    """
    if not path.exists():
        return []
    patterns: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if not parts:
            continue
        pat = parts[0]
        if pat.startswith("!"):
            # Negation pattern — skip; full gitignore semantics out of scope.
            continue
        if pat.startswith("/"):
            pat = pat[1:]
        patterns.append(pat)
    return patterns


def matches_codeowner(path: str, patterns: list[str]) -> str | None:
    """Return the first matching CODEOWNERS pattern, or None."""
    for pat in patterns:
        if pat.endswith("/"):
            # Directory pattern: matches anything under that prefix
            if path.startswith(pat) or fnmatch.fnmatch(path, pat + "*"):
                return pat
        elif pat.startswith("*"):
            if fnmatch.fnmatch(path, pat):
                return pat
        else:
            # Exact path or directory-style
            if path == pat or path.startswith(pat + "/") or fnmatch.fnmatch(path, pat):
                return pat
    return None


def get_changed_files(args: argparse.Namespace) -> list[str]:
    if args.changed_files:
        return [
            line.strip()
            for line in Path(args.changed_files).read_text().splitlines()
            if line.strip()
        ]
    base = os.environ.get("BASE_SHA")
    head = os.environ.get("HEAD_SHA")
    if base and head:
        cmd = ["git", "diff", "--name-only", base, head]
    else:
        cmd = ["git", "diff", "--name-only", "origin/main...HEAD"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return [line for line in result.stdout.splitlines() if line.strip()]
    except FileNotFoundError:
        print("ERROR: `git` not available; cannot compute diff.", file=sys.stderr)
        return []


def get_pr_body(args: argparse.Namespace) -> str:
    if args.pr_body:
        return Path(args.pr_body).read_text(encoding="utf-8")
    return os.environ.get("PR_BODY", "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-body", help="Path to a file containing the PR body")
    parser.add_argument(
        "--changed-files",
        help="Path to a file with one changed-file path per line",
    )
    args = parser.parse_args()

    codeowners_path = ROOT / ".github" / "CODEOWNERS"
    patterns = parse_codeowners(codeowners_path)
    if not patterns:
        print(
            f"ERROR: no patterns in {codeowners_path}; rail-guard cannot operate.",
            file=sys.stderr,
        )
        return 2

    body = get_pr_body(args)
    rail_match = RAIL_RE.search(body)
    if not rail_match:
        print("FAIL: no `Rail: green|amber|red` declaration found in PR body.")
        print("      Add a line `Rail: green` (or amber/red) to the PR description.")
        return 1
    rail = rail_match.group(1).lower()

    changed = get_changed_files(args)
    if not changed:
        print("INFO: no changed files detected; rail-guard skipping.")
        return 0

    sensitive_hits = []
    for f in changed:
        pat = matches_codeowner(f, patterns)
        if pat:
            sensitive_hits.append((f, pat))

    if rail == "green" and sensitive_hits:
        print("FAIL: PR declared `Rail: green` but touches CODEOWNERS paths:")
        for f, pat in sensitive_hits[:10]:
            print(f"  - {f}  (matches `{pat}`)")
        if len(sensitive_hits) > 10:
            print(f"  ... and {len(sensitive_hits) - 10} more.")
        print("\nReclassify the rail to `amber` or `red` in the PR body and push again.")
        return 1

    note = (
        f" ({len(sensitive_hits)} under CODEOWNERS)" if sensitive_hits else ""
    )
    print(f"OK: rail `{rail}` consistent with {len(changed)} changed file(s){note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
