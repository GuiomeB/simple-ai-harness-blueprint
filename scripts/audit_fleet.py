#!/usr/bin/env python3
"""audit_fleet.py — fleet-wide doctrine audit for harnessed repos.

Scans a root directory (default: ~/Dev) for `AGENTS.md` files and reports,
per repo: doctrine version stamp, AGENTS.md line count, inferred harness
size, learning-loop usage (docs/learn + docs/retro entries), and last git
commit date. Read-only: writes nothing, prints a Markdown table to stdout.

Usage:
    python scripts/audit_fleet.py [root]

Exit code: always 0 (informational tool, not a gate).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

PRUNED_DIRS = {".git", "node_modules", "_archives", ".claude"}
TEMPLATE_MARKER = os.sep + os.path.join("references", "templates") + os.sep
STAMP = re.compile(r"^> Doctrine:\s*(v\d+\S*)", re.MULTILINE)


def find_harnessed_repos(root: Path) -> list[Path]:
    """Return directories containing an AGENTS.md, excluding pruned zones.

    Args:
        root: Directory tree to scan.

    Returns:
        Sorted list of repo directories (parents of each AGENTS.md found).
    """
    repos: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNED_DIRS]
        if TEMPLATE_MARKER in dirpath + os.sep:
            continue
        if "AGENTS.md" in filenames:
            repos.append(Path(dirpath))
    return sorted(repos)


def doctrine_version(agents_md: Path) -> str:
    """Extract the doctrine version stamp from an AGENTS.md.

    Args:
        agents_md: Path to the AGENTS.md file.

    Returns:
        The stamped version (e.g. "v5", "v4"), or "inconnue" when the file
        carries no `> Doctrine:` stamp line.
    """
    match = STAMP.search(agents_md.read_text(encoding="utf-8"))
    return match.group(1) if match else "inconnue"


def inferred_size(repo: Path) -> str:
    """Infer the harness size from the .agents/ tree (L > M > S)."""
    if (repo / ".agents" / "patterns").is_dir():
        return "L"
    if (repo / ".agents" / "ROUTER.md").is_file():
        return "M"
    return "S"


def doc_entries(repo: Path, family: str) -> int:
    """Count real entries (non-README .md files) under docs/<family>/."""
    folder = repo / "docs" / family
    if not folder.is_dir():
        return 0
    return sum(1 for p in folder.glob("*.md") if p.name != "README.md")


def last_commit_date(repo: Path) -> str:
    """Return the last git commit date (YYYY-MM-DD), or "—" without git."""
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%cs"],
        capture_output=True,
        text=True,
    )
    date = result.stdout.strip()
    return date if result.returncode == 0 and date else "—"


def main() -> int:
    """Scan the fleet and print the audit table."""
    root = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / "Dev"
    if not root.is_dir():
        print(f"audit_fleet: root introuvable: {root}", file=sys.stderr)
        return 0

    print(f"# Audit flotte — {root}\n")
    print("| Repo | Doctrine | AGENTS.md (lignes) | Taille | learn | retro | Dernier commit |")
    print("|---|---|---|---|---|---|---|")
    for repo in find_harnessed_repos(root):
        agents_md = repo / "AGENTS.md"
        lines = len(agents_md.read_text(encoding="utf-8").splitlines())
        print(
            f"| {repo.relative_to(root)} "
            f"| {doctrine_version(agents_md)} "
            f"| {lines} "
            f"| {inferred_size(repo)} "
            f"| {doc_entries(repo, 'learn')} "
            f"| {doc_entries(repo, 'retro')} "
            f"| {last_commit_date(repo)} |"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
