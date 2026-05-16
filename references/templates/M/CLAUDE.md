# <Project Name> — Claude adapter

> Include this file **only if Claude (Claude Code or Claude.ai) is one of the agents working on this repo**. Otherwise delete it — `AGENTS.md` already carries everything universal.

## Doctrine

The 4 Karpathy rules and all project doctrine live in **`AGENTS.md`** — read it first, every session. Never duplicate them here.

## Role of this file

- This is a thin adapter for Claude (Claude Code, Claude.ai, future Claude IDE integrations).
- It restates the load order Claude must follow at size M.
- If a rule appears in both files, `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (the project contract — implicit, never skip)
2. `.agents/ROUTER.md` (identify task family, pick the minimum context)
3. the capsule / pattern the router points to (if any)
4. the files directly touched by the request
5. additional documentation only if the router points to it

Never load large documents "just in case". Use progressive disclosure.

## Conditional context loading (Claude-specific shortcuts)

For common change shapes, you may pre-fetch:

- change in `<critical-zone-1>` → load `.agents/context/<domain-1>.md` first
- change in `<critical-zone-2>` → load `.agents/context/<domain-2>.md` first
- change to agent memory (`AGENTS.md`, `.agents/**`, `WORKFLOW.md`) → re-check internal links after edit

Add one bullet per stable shortcut as it emerges. If a shortcut is used in 3+ sessions, promote it to a row in `.agents/ROUTER.md`.

## Claude-specific reminders

- Start with read-only exploration around the critical files before editing — never blind-write.
- After completing any task, declare a `Rail: green | amber | red` in your final message and in the PR body (template at `.github/pull_request_template.md`).
- For a recurring friction, an incident, or a meaningful refactor, invoke `/learn <family> <slug>` (workflow at `.agents/workflows/learning-loop.md`).
- For a release of a cycle (within 24h), invoke `/retro <YYYY-MM-DD>` (workflow at `.agents/workflows/retro.md`).
- Keep this file ≤ 60 lines. If doctrine starts to accrete here, move it to `AGENTS.md` or to a capsule under `.agents/context/`.
