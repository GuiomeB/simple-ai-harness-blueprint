# <Project Name>

<One-paragraph description of what the project does.>

## Quick start

```bash
<setup commands — install, dev server, test, etc.>
```

## Stack

- <language / framework>
- <runtime / hosting>
- <data layer, if any>

## Working with AI agents on this repo

This repo follows the [Simple AI Harness Blueprint](https://github.com/<owner>/simple-ai-harness-blueprint) at size **M**.

Before generating or modifying code, any AI agent (Cursor, Claude Code, Windsurf, Codex CLI, Antigravity, Copilot, …) must:

1. Read `AGENTS.md` (the universal contract — 5 Karpathy rules + M0 + critical zones + commands).
2. Open `.agents/ROUTER.md` and load the minimum context for the task family at hand.
3. Declare a **risk rail** (`green` / `amber` / `red`) in the final message and in the PR body (template at `.github/pull_request_template.md`).

When a friction recurs, an incident happens, or a meaningful refactor lands, invoke `/learn` (`.agents/workflows/learning-loop.md`). After every release of a cycle, invoke `/retro <YYYY-MM-DD>` (`.agents/workflows/retro.md`). One action retained, lands in the right file — the system improves itself.

## Project status

Current state, recent decisions, and release checklist live in `STATUS_APP.md`.

## License

<TBD — e.g. MIT, Apache-2.0.>
