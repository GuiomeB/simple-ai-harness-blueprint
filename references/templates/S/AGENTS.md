# <Project Name> — Agent Contract

## Doctrine — the 4 Karpathy rules

Before any action on this repo, **every agent** (Claude, Codex CLI, Cursor, Antigravity, Copilot, …) applies these rules in order. They override convenience and any other rule in this file when conflicts arise.

1. **Don't assume. Don't hide confusion. Surface trade-offs.**
   If intent is ambiguous (format, scope, fields, target, environment), ask before writing code. Make trade-offs explicit — never make silent choices.

2. **Minimal code that solves the problem. Nothing speculative.**
   No preventive abstractions. No Strategy pattern for five lines of arithmetic.

3. **Touch only what's necessary. Clean up only your own traces.**
   Diff = scope of the ticket. No opportunistic reformatting, no collateral renames, no "improvements on the side". Clean orphans *your* changes created. Leave pre-existing dead code alone unless explicitly asked.

4. **Define success criteria. Loop until verified.**
   State the verifiable criterion (red test going green, lint pass, smoke command) before acting. Iterate until it passes.

## Role of this file

- `AGENTS.md` is the canonical source of truth for project-wide rules shared by all agents.
- If a project-specific agent-adapter file exists (`CLAUDE.md`, `GEMINI.md`, etc.), it is a *thin adapter*. It must not duplicate this file — only restate the load order.
- If a rule conflicts: `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (this file) — implicit, never skip.
2. The files directly touched by the request.
3. Additional documentation only if the task obviously requires it.

Never load large documents "just in case". Use progressive disclosure.

(At size M, step 2 becomes `.agents/ROUTER.md`. Don't pre-create it at S.)

## Project

<2–4 lines of context an agent cannot deduce from the code itself: domain, deployment target, any unusual architectural choice.>

## Essential commands

```bash
<run dev>                 # local dev server
<typecheck>               # type checker
<lint>                    # linter
<test>                    # unit tests
<format>                  # formatter — run before every commit
<build>                   # production build
```

## Critical zones

Files where mistakes are expensive. Edit only with explicit success criteria and tests.

| File | Why it's critical | Required validation |
|---|---|---|
| `<path/to/file.ts>` | <one-line reason> | <command or test> |
| `<path/to/file.ts>` | <one-line reason> | <command or test> |

If you must touch one of these, state your success criterion **before** editing.

## Minimal validation matrix

For each kind of change, the minimum command(s) the agent must run before declaring a task done. Knowing the zones isn't enough — agents must know *how to prove* the work holds.

| Change family | When it applies | Minimum validation |
|---|---|---|
| UI / surface change | component, style, visible text | `<format>`, `<lint>`, `<typecheck>`, targeted test if behaviour changed |
| Business logic | domain code, data transformations | `<typecheck>` + targeted tests |
| Runtime / config / env | env vars, build config, deployment scripts | `<typecheck>` + smoke or integration command |
| Documentation only | `.md` files, this file, README | no code validation; check internal links resolve |

If a change spans multiple families, run the union of validations.

## Risk rail (declare after every task)

After completing any task — and before pushing or committing — declare a rail in your message:

- **Rail: green | amber | red**

| Rail | Meaning |
|---|---|
| `green` | small/local change; no critical zone touched; safe to merge fast |
| `amber` | behavioural or transverse change; the user should scan the diff |
| `red` | critical path or production risk; the user must review carefully |

The rail is informational at S (no CI enforcement). Its value is forcing the agent to self-assess sensitivity, and letting the user see it in one glance.

## Learning loop

When a friction recurs (the same kind of mistake twice, an incident, a no-go release, a meaningful refactor), invoke the `/learn` workflow defined in `.agents/workflows/learning-loop.md`. One action retained, lands in the right file. Don't let frictions die unrecorded.

## Promotion criterion to size M

Adopt M when **two or more** of the following are true:

- This `AGENTS.md` has grown beyond ~150 lines of *project-specific* accretion (excluding the universal baseline).
- The same domain has produced "the agent forgot rule X" frictions three or more times.
- You routinely use two or more different AI agents on this repo.
- You've started a PR workflow (GitHub-style or equivalent).

When promoting: don't rename anything. Add `STATUS_APP.md`, `.agents/ROUTER.md`, one or two `.agents/context/<domain>.md` capsules, and `.github/pull_request_template.md`. Move domain-specific rules out of this file into the capsules.
