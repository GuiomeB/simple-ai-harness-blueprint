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

This repo follows the [Simple AI Harness Blueprint](https://github.com/<owner>/simple-ai-harness-blueprint) at size **L** — the full system, with machine-enforced risk rails and a meta-validator.

Before generating or modifying code, any AI agent (Cursor, Claude Code, Windsurf, Codex CLI, Antigravity, Copilot, …) must:

1. Read `AGENTS.md` (the universal contract — 4 Karpathy rules + critical zones + commands).
2. Open `.agents/ROUTER.md` and load the minimum context for the task at hand (capsule + pattern if any).
3. Declare a **risk rail** (`green` / `amber` / `red`) in the PR body. The CI gate `pr-rail-guard` fails `green` PRs that touch `.github/CODEOWNERS` paths.

After every diffusion that touches `AGENTS.md`, `.agents/**`, or `WORKFLOW.md`, run `python scripts/validate_agent_context.py`.

## Learning loop

- After every release of a cycle: `/retro <YYYY-MM-DD>` — workflow at `.agents/workflows/retro.md`.
- After incidents, recurring frictions, refactors, or blocked candidates: `/learn <family> <slug>` — workflow at `.agents/workflows/learning-loop.md`.

Hard constraint in both: **one action retained**, lands in the right artefact, validator re-run after diffusion.

## Project status

Current state, recent decisions, and release checklist live in `STATUS_APP.md`. Major decisions are recorded as ADRs under `docs/adr/`.

## License

<TBD — e.g. MIT, Apache-2.0.>
