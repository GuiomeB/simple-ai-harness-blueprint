# <Project Name> — Claude adapter

> Include this file **only if Claude (Claude Code or Claude.ai) is one of the agents working on this repo**. Otherwise delete it.

## Doctrine

The 5 Karpathy rules (+ the M0 verification mechanism) and all project doctrine live in **`AGENTS.md`** — read it first, every session. Never duplicate them here.

## Role of this file

- Thin adapter for Claude.
- Restates the load order Claude must follow at size L (the L+ profile adds `/loop`; see `AGENTS.md §Autonomy profile`).
- If a rule appears in both files, `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (the project contract — implicit, never skip)
2. `.agents/ROUTER.md` (identify task family, pick the minimum context)
3. the capsule and/or pattern the router points to (if any)
4. the files directly touched by the request
5. additional documentation only if the router points to it

Never load large documents "just in case". Never load more than 3 capsules + patterns simultaneously.

## Conditional context loading (Claude-specific shortcuts)

- change in `<critical-zone-1>` → load `.agents/context/<domain-1>.md` + (if procedure recurs) `.agents/patterns/<pattern>.md`
- change in `<critical-zone-2>` → load `.agents/context/<domain-2>.md` + relevant pattern
- change to agent memory (`AGENTS.md`, `.agents/**`, `WORKFLOW.md`) → after edit, run `python scripts/validate_agent_context.py`

Add one bullet per stable shortcut as it emerges. If a shortcut recurs in 3+ sessions, promote it to a row in `.agents/ROUTER.md`.

## Claude-specific reminders

- Start with read-only exploration around the critical files before editing.
- After every task, declare a `Rail: green | amber | red` in the PR body (template at `.github/pull_request_template.md`). The CI gate `pr-rail-guard` will fail mismatched declarations against `.github/CODEOWNERS`.
- After a recurring friction, an incident, or a meaningful refactor, invoke `/learn <family> <slug>`.
- After every release of a cycle (within 24h), invoke `/retro <YYYY-MM-DD>`.
- After every diffusion that touches `.agents/**` or `AGENTS.md`, re-run the validator.
- Keep this file ≤ 60 lines. If doctrine starts to accrete here, move it to `AGENTS.md` or a capsule.
