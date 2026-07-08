#!/usr/bin/env python3
"""validate_agent_context.py — meta-validator for the AI harness blueprint.

Checks (in order):
  1. Every internal Markdown link in AGENTS.md, CLAUDE.md, WORKFLOW.md, and
     under .agents/** resolves to an existing path.
  2. Every `.md` file under .agents/patterns/ (except INDEX.md) is referenced
     in .agents/patterns/INDEX.md, and vice versa.
  3. Every capsule referenced from .agents/ROUTER.md exists under
     .agents/context/.
  4. `.claude/` runtime adapter (agents frontmatter, settings.json hooks,
     AGENTS.md inline refs).
  5. `.agents/**` doctrine uses tier vocabulary, not concrete model names
     (warning via `check_hardcoded_models()`).
  6. Every `npm run X` or `python scripts/X.py` cited in AGENTS.md / WORKFLOW.md
     points to something callable (best-effort: checks package.json scripts
     and file existence; skips silently if neither resource is available).

Exit code:
  0 — all checks pass
  1 — at least one warning (missing optional pieces)
  2 — at least one error (broken internal link, orphan pattern, missing capsule)

Run from the repo root. No external dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
errors: list[str] = []
warnings: list[str] = []

MD_LINK = re.compile(r"\[[^\]]+\]\(([^)#]+?)(?:#[^)]*)?\)")
INLINE_PATH = re.compile(r"`([^`]+\.(?:md|py|ts|tsx|yml|yaml|json|sh))`")
NPM_CMD = re.compile(r"`npm run ([a-zA-Z0-9:_\-]+)`")
PY_CMD = re.compile(r"`python (scripts/[\w/\-.]+\.py)`")
HARD_MODEL = re.compile(
    r"\b(opus|sonnet|haiku|gpt-\d|gemini-\d|o[13]-)\b", re.IGNORECASE
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def check_links_in(md_path: Path) -> None:
    """Verify every relative Markdown link in `md_path` resolves."""
    if not md_path.exists():
        return
    text = read_text(md_path)
    for match in MD_LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        # Skip template placeholders like `<owner>` or `<NNNN>`
        if "<" in target or ">" in target:
            continue
        # Resolve relative to the .md file
        candidate = (md_path.parent / target).resolve()
        if not candidate.exists():
            errors.append(
                f"Broken link in {md_path.relative_to(ROOT)}: -> {target}"
            )


def check_patterns_index() -> None:
    """Every pattern .md is in INDEX.md and vice versa."""
    patterns_dir = ROOT / ".agents" / "patterns"
    index = patterns_dir / "INDEX.md"
    if not patterns_dir.exists():
        return
    if not index.exists():
        if any(patterns_dir.glob("*.md")):
            errors.append(
                ".agents/patterns/ contains files but INDEX.md is missing"
            )
        return

    on_disk = {
        p.name for p in patterns_dir.glob("*.md") if p.name != "INDEX.md"
    }
    index_text = read_text(index)
    referenced = set()
    for match in MD_LINK.finditer(index_text):
        target = match.group(1).strip().lstrip("./")
        if target.endswith(".md"):
            referenced.add(target)

    orphans_on_disk = on_disk - referenced
    orphans_in_index = referenced - on_disk

    for orphan in sorted(orphans_on_disk):
        errors.append(
            f"Pattern .agents/patterns/{orphan} exists but is not in INDEX.md"
        )
    for ghost in sorted(orphans_in_index):
        errors.append(
            f"INDEX.md references .agents/patterns/{ghost} which does not exist"
        )


def check_router_capsules() -> None:
    """Every capsule referenced from ROUTER.md exists."""
    router = ROOT / ".agents" / "ROUTER.md"
    if not router.exists():
        return
    text = read_text(router)
    for match in INLINE_PATH.finditer(text):
        ref = match.group(1).strip()
        if not ref.startswith("context/"):
            continue
        # Skip template placeholders
        if "<" in ref or ">" in ref:
            continue
        candidate = ROOT / ".agents" / ref
        if not candidate.exists():
            warnings.append(
                f"ROUTER.md references .agents/{ref} which does not exist"
            )


def check_claude_artifacts() -> None:
    """Validate the Claude-Code runtime adapter under .claude/ (L+ execution primitives).

    - Every .claude/agents/*.md must carry YAML frontmatter with name/tools/model.
    - .claude/settings.json (if present) must be valid JSON, and every hook
      `command` that points at a .claude/ script must resolve on disk.
    - Every `.claude/agents/<x>.md` cited inline in AGENTS.md must exist.
    """
    claude = ROOT / ".claude"
    if not claude.exists():
        return

    agents_dir = claude / "agents"
    if agents_dir.exists():
        for agent in sorted(agents_dir.glob("*.md")):
            text = read_text(agent)
            if not text.startswith("---"):
                errors.append(
                    f".claude/agents/{agent.name} is missing YAML frontmatter"
                )
                continue
            head = text.split("---", 2)[1] if text.count("---") >= 2 else ""
            for key in ("name:", "description:", "tools:", "model:"):
                if key not in head:
                    warnings.append(
                        f".claude/agents/{agent.name} frontmatter has no `{key}`"
                    )

    settings = claude / "settings.json"
    if settings.exists():
        try:
            data = json.loads(read_text(settings))
        except json.JSONDecodeError as exc:
            errors.append(f".claude/settings.json is not valid JSON: {exc}")
        else:
            for cmd in re.findall(r'"command"\s*:\s*"([^"]+)"', json.dumps(data)):
                token = cmd.split()[0] if cmd else ""
                if token.startswith(".claude/") and not (ROOT / token).exists():
                    errors.append(
                        f".claude/settings.json references hook `{token}` "
                        f"which does not exist"
                    )

    agents_md = ROOT / "AGENTS.md"
    if agents_md.exists():
        for match in INLINE_PATH.finditer(read_text(agents_md)):
            ref = match.group(1).strip()
            if ref.startswith(".claude/agents/") and "<" not in ref:
                if not (ROOT / ref).exists():
                    errors.append(
                        f"AGENTS.md references {ref} which does not exist"
                    )


def check_hardcoded_models() -> None:
    """Warn when `.agents/**` doctrine names concrete models (tiers only)."""
    agents = ROOT / ".agents"
    if not agents.exists():
        return
    for md in sorted(agents.rglob("*.md")):
        text = read_text(md)
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if HARD_MODEL.search(line):
                warnings.append(
                    f"{md.relative_to(ROOT)}:{lineno} names a concrete model; "
                    f"use tier vocabulary (top/mid/low/cross-family)"
                )


def check_commands() -> None:
    """Verify cited `npm run X` and `python scripts/X.py` commands exist."""
    pkg = ROOT / "package.json"
    npm_scripts: set[str] = set()
    if pkg.exists():
        try:
            data = json.loads(read_text(pkg))
            npm_scripts = set((data.get("scripts") or {}).keys())
        except json.JSONDecodeError:
            warnings.append("package.json is not valid JSON")

    for md_name in ("AGENTS.md", "WORKFLOW.md", "CLAUDE.md"):
        path = ROOT / md_name
        if not path.exists():
            continue
        text = read_text(path)
        if pkg.exists():
            for match in NPM_CMD.finditer(text):
                script = match.group(1)
                if script not in npm_scripts:
                    warnings.append(
                        f"{md_name} cites `npm run {script}` but it is not in "
                        f"package.json scripts"
                    )
        for match in PY_CMD.finditer(text):
            rel = match.group(1)
            if not (ROOT / rel).exists():
                warnings.append(
                    f"{md_name} cites `python {rel}` but the file does not exist"
                )


def collect_doc_files() -> list[Path]:
    """All .md files this validator should sanity-check for links."""
    roots = [
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "WORKFLOW.md",
        ROOT / "STATUS_APP.md",
        ROOT / "README.md",
    ]
    files = [p for p in roots if p.exists()]
    for subdir in (".agents", ".claude", "docs"):
        d = ROOT / subdir
        if d.exists():
            files.extend(d.rglob("*.md"))
    return files


def main() -> int:
    for md in collect_doc_files():
        check_links_in(md)
    check_patterns_index()
    check_router_capsules()
    check_claude_artifacts()
    check_hardcoded_models()
    check_commands()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
        return 2
    if warnings:
        print(f"\n{len(warnings)} warning(s), 0 errors.")
        return 1
    print("validate_agent_context: all checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
