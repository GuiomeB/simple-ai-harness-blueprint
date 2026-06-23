# simple-ai-harness-blueprint — Claude adapter

> Claude Code is the primary agent for this repo. Codex CLI also operates here and reads `AGENTS.md` natively — no Codex-specific adapter is needed.

## Doctrine

The 5 Karpathy rules (+ the M0 verification mechanism) and all project doctrine live in **`AGENTS.md`** — read it first, every session. Never duplicate them here.

## Role of this file

- Thin adapter for Claude Code.
- Restates the load order Claude must follow at size L.
- If a rule appears in both files, `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (the project contract — implicit, never skip)
2. `.agents/ROUTER.md` (identify task family, pick the minimum context)
3. the capsule and/or pattern the router points to (if any)
4. the files directly touched by the request
5. additional documentation only if the router points to it

Never load large documents "just in case". Never load more than 3 capsules + patterns simultaneously.

## Conditional context loading (Claude-specific shortcuts)

- change in `AGENTS.md`, `.agents/**`, `WORKFLOW.md`, or `scripts/validate_agent_context.py` → after edit, run `python scripts/validate_agent_context.py`
- change in `.github/workflows/pr-rail-guard.yml` or `scripts/check_pr_rail_consistency.py` → load `.agents/patterns/change-critical-zone.md`; reason about CODEOWNERS coverage before editing
- change in a template under `.agents/`, `docs/adr/`, `_local/` that ships to downstream users → mentally dry-run a copy into a fresh repo before declaring done

Add one bullet per stable shortcut as it emerges. If a shortcut recurs in 3+ sessions, promote it to a row in `.agents/ROUTER.md`.

## Claude-specific reminders

- Start with read-only exploration around the critical files before editing.
- After every task, declare a `Rail: green | amber | red` in the PR body (template at `.github/pull_request_template.md`). The CI gate `pr-rail-guard` will fail mismatched declarations against `.github/CODEOWNERS`.
- After a recurring friction, an incident, or a meaningful refactor, invoke `/learn <family> <slug>`.
- After every release of a cycle (within 24h), invoke `/retro <YYYY-MM-DD>`.
- After every diffusion that touches `.agents/**` or `AGENTS.md`, re-run the validator.
- Keep this file ≤ 60 lines. If doctrine starts to accrete here, move it to `AGENTS.md` or a capsule.
