"""Tests for scripts/check_pr_rail_consistency.py (the blocking `pr-rail-guard`).

Each test runs the real script as a subprocess inside a throwaway git
repository, so the real `git diff` path is exercised (bad SHA, git missing,
empty diff) instead of a mocked subprocess. #16 was a fail-open bug on exactly
that path; a mock would have hidden it.

Run: python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_pr_rail_consistency.py"
TEMPLATE_COPIES = [
    REPO_ROOT / "references" / "templates" / "L" / "scripts" / SCRIPT.name,
    REPO_ROOT / "references" / "templates" / "L+" / "scripts" / SCRIPT.name,
]

CODEOWNERS = "# critical paths\nscripts/  @owner\n.github/workflows/  @owner\n"
UNRESOLVABLE_SHA = "0" * 40


def _git_env() -> dict[str, str]:
    """Environment isolated from the developer's git config and from CI vars."""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PR_BODY", "BASE_SHA", "HEAD_SHA"}
    }
    env.update(
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_CONFIG_NOSYSTEM="1",
        GIT_AUTHOR_NAME="test",
        GIT_AUTHOR_EMAIL="test@example.invalid",
        GIT_COMMITTER_NAME="test",
        GIT_COMMITTER_EMAIL="test@example.invalid",
    )
    return env


class RailGuardTestCase(unittest.TestCase):
    """Builds a temp repo: a base commit with CODEOWNERS, then a head commit."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = Path(self._tmp.name)
        self.env = _git_env()
        self._git("init", "-q")
        self._write(".github/CODEOWNERS", CODEOWNERS)
        self._write("README.md", "base\n")
        self.base = self._commit("base")

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def _write(self, relpath: str, content: str) -> None:
        path = self.repo / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _commit(self, message: str) -> str:
        self._git("add", "-A")
        self._git("commit", "-q", "--allow-empty", "-m", message)
        return self._git("rev-parse", "HEAD")

    def _change(self, relpath: str) -> str:
        """Commit a change to `relpath` on top of base; return the head SHA."""
        self._write(relpath, "changed\n")
        return self._commit(f"change {relpath}")

    def run_guard(
        self,
        body: str,
        base: str | None = None,
        head: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        run_env = dict(env if env is not None else self.env)
        run_env["PR_BODY"] = body
        if base is not None:
            run_env["BASE_SHA"] = base
        if head is not None:
            run_env["HEAD_SHA"] = head
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.repo,
            env=run_env,
            capture_output=True,
            text=True,
            check=False,
        )


class GitDiffFailureTests(RailGuardTestCase):
    def test_unresolvable_base_sha_exits_2_with_git_error(self) -> None:
        head = self._change("docs/note.md")
        result = self.run_guard("Rail: green", base=UNRESOLVABLE_SHA, head=head)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("cannot compute diff", result.stderr)
        # git's own message is forwarded, not swallowed.
        self.assertIn("fatal:", result.stderr)

    def test_git_not_on_path_exits_2(self) -> None:
        head = self._change("docs/note.md")
        env = dict(self.env)
        with tempfile.TemporaryDirectory() as empty_dir:
            env["PATH"] = empty_dir
            result = self.run_guard("Rail: green", base=self.base, head=head, env=env)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("`git` not available", result.stderr)


class RailDeclarationTests(RailGuardTestCase):
    def test_green_rail_touching_codeowners_path_exits_1(self) -> None:
        head = self._change("scripts/tool.py")
        result = self.run_guard("Rail: green", base=self.base, head=head)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("scripts/tool.py", result.stdout)

    def test_amber_or_red_rail_touching_codeowners_path_exits_0(self) -> None:
        head = self._change("scripts/tool.py")
        for rail in ("amber", "red"):
            with self.subTest(rail=rail):
                result = self.run_guard(f"Rail: {rail}", base=self.base, head=head)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_green_rail_outside_codeowners_exits_0(self) -> None:
        head = self._change("docs/note.md")
        result = self.run_guard("Rail: green", base=self.base, head=head)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_or_placeholder_rail_exits_1(self) -> None:
        head = self._change("docs/note.md")
        bodies = {
            "no rail line": "## Summary\nSome change.\n",
            "template placeholder": "- **Rail: green | amber | red**\n",
        }
        for label, body in bodies.items():
            with self.subTest(case=label):
                result = self.run_guard(body, base=self.base, head=head)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


class EdgeCaseTests(RailGuardTestCase):
    def test_genuinely_empty_diff_exits_0(self) -> None:
        result = self.run_guard("Rail: green", base=self.base, head=self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no changed files", result.stdout)

    def test_missing_or_empty_codeowners_exits_2(self) -> None:
        head = self._change("scripts/tool.py")
        codeowners = self.repo / ".github" / "CODEOWNERS"
        for label in ("empty (comments only)", "missing"):
            with self.subTest(case=label):
                if label == "missing":
                    codeowners.unlink()
                else:
                    codeowners.write_text("# nothing here\n", encoding="utf-8")
                result = self.run_guard("Rail: green", base=self.base, head=head)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("rail-guard cannot operate", result.stderr)


class TemplateCopiesTests(unittest.TestCase):
    def test_template_copies_are_byte_identical(self) -> None:
        # The templates ship the same gate; these tests only cover the root
        # copy, so the copies must not drift from it.
        expected = SCRIPT.read_bytes()
        for copy in TEMPLATE_COPIES:
            with self.subTest(copy=str(copy.relative_to(REPO_ROOT))):
                self.assertEqual(copy.read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
