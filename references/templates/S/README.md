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

This repo follows the [Simple AI Harness Blueprint](https://github.com/<owner>/simple-ai-harness-blueprint) at size **S**.

Any AI agent (Cursor, Claude Code, Windsurf, Codex CLI, Antigravity, Copilot, …) **must read `AGENTS.md` first** before generating or modifying code. The 4 universal rules and the project's critical zones live there.

After every task, the agent declares a **risk rail** (`green` / `amber` / `red`) so you can see the sensitivity of what was touched. The rail rule is in `AGENTS.md §Risk rail`.

When a friction recurs or a meaningful refactor happens, run the `/learn` workflow defined in `.agents/workflows/learning-loop.md`. One action, lands in the right file, the system improves.

## License

<TBD — e.g. MIT, Apache-2.0.>
