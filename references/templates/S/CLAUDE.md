# <Project Name> — Claude adapter

> Include this file **only if Claude (Claude Code or Claude.ai) is one of the agents working on this repo**. Otherwise delete it — `AGENTS.md` already carries everything universal.

## Doctrine

The 4 Karpathy rules and all project doctrine live in **`AGENTS.md`** — read it first, every session. Never duplicate them here.

## Role of this file

- This is a thin adapter for Claude (Claude Code, Claude.ai, future Claude IDE integrations).
- It does not replace `AGENTS.md`; it only restates the load order Claude must follow.
- If a rule appears in both files, `AGENTS.md` wins.

## Context loading order (every new request)

Before generating code for any new request, always load context in this order:

1. `AGENTS.md` (the project contract — implicit, never skip)
2. The files directly touched by the request
3. Additional documentation only if the task obviously requires it

Never load large documents "just in case". Use progressive disclosure.

## Claude-specific reminders

- After completing any task, declare a `Rail: green | amber | red` in your message (see `AGENTS.md §Risk rail`).
- If a friction repeats or a meaningful refactor happens, invoke the `/learn` workflow defined in `.agents/workflows/learning-loop.md`. Don't let it die unrecorded.
- Keep this file under ~60 lines. If you find yourself adding doctrine here, move it to `AGENTS.md` or, at size M, to a capsule under `.agents/context/`.
