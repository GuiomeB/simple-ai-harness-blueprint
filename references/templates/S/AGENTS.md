# <Project Name> — Agent Contract

## Doctrine — the 5 Karpathy rules

Before any action on this repo, **every agent** (Claude, Codex CLI, Cursor, Antigravity, Copilot, …) applies these rules in order. They override convenience and any other rule in this file when conflicts arise. They are *posture*; the verification mechanism is **M0** (below).

1. **Ask, don't assume.**
   If anything is unclear (format, scope, fields, target, environment, architecture), ask before writing a single line. Never make silent assumptions. *Only* when running unattended in an explicitly activated autonomous mode (L+), pick the most reasonable interpretation, proceed, and **record the assumption** rather than blocking.

2. **Simplest solution for simple problems, stronger solutions for hard ones.**
   Match the solution to the difficulty. Don't over-engineer or add flexibility that isn't needed yet. No preventive abstractions. No Strategy pattern for five lines of arithmetic.

3. **Don't touch unrelated code — but surface what you find.**
   Diff = scope of the ticket. No opportunistic reformatting, no collateral renames, no "improvements on the side". When you spot bad code or a design smell, raise it with the user as a *separate* issue instead of fixing it inline. Clean orphans *your* changes created.

4. **Flag uncertainty explicitly.**
   If you're unsure, see rule 1. When it makes sense, run a small, localised, low-risk experiment and bring the hypothesis and results back to discuss. Confidence without certainty does more damage than admitting a gap.

5. **Suggest better ways.**
   Stay open to improvements. Propose a better approach — especially one with lasting impact over a tactical fix — rather than silently taking the first path.

## M0 — Verification (the mechanism behind every task)

The 5 rules are posture; **M0 is the mechanism every task inherits.** Before acting, state a **verifiable success criterion** (red test going green, lint pass, smoke command), then loop until it holds: **trigger** · **stop criterion** · **validation** (§Minimal validation matrix) · **budget** (time / iterations) · **stop / no-progress** (stop and surface the blocker per rule 1 instead of looping blindly). The validation matrix and the Definition of Done both inherit from M0.

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
