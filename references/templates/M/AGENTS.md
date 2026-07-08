# <Project Name> — Agent Contract

> Doctrine: v5 (5 règles Karpathy + M0) — appliquée <YYYY-MM-DD>

## Doctrine — the 5 Karpathy rules

Before any action on this repo, **every agent** (Claude, Codex CLI, Cursor, Antigravity, Copilot, …) applies these rules in order. They override convenience and any other rule in this file when conflicts arise. They are *posture*; the verification mechanism is **M0** (below).

1. **Ask, don't assume.**
   If anything is unclear — intent, architecture, requirements — ask before writing a single line. Never make silent assumptions. *Only* when running unattended in an explicitly activated autonomous mode (L+), pick the most reasonable interpretation, proceed, and **record the assumption** rather than blocking.

2. **Simplest solution for simple problems, stronger solutions for hard ones.**
   Match the solution to the difficulty. Don't over-engineer or add flexibility that isn't needed yet. No preventive abstractions.

3. **Don't touch unrelated code — but surface what you find.**
   Diff = scope of the ticket. No opportunistic edits. When you spot bad code or a design smell, raise it with the user as a *separate* issue instead of fixing it inline.

4. **Flag uncertainty explicitly.**
   If you're unsure, see rule 1. When it makes sense, run a small, localised, low-risk experiment and bring the hypothesis and results back to discuss. Confidence without certainty does more damage than admitting a gap.

5. **Suggest better ways.**
   Stay open to improvements. Propose a better approach — especially one with lasting impact over a tactical fix — rather than silently taking the first path.

## M0 — Verification (the mechanism behind every task)

The 5 rules are posture; **M0 is the mechanism every task inherits.** Before acting, state a **verifiable success criterion**, then loop until it holds. Operational form: **trigger** (what starts the work) · **stop criterion** (red test → green, lint clean, smoke passes) · **validation** (the minimum commands from §Minimal validation matrix) · **budget** (time / iterations) · **stop / no-progress** (stop and surface the blocker per rule 1 instead of looping blindly).

The validation matrix, the Definition of Done (`WORKFLOW.md`), and `/tdd-loop` all inherit from M0.

## Role of this file

- `AGENTS.md` is the canonical contract for all agents.
- Domain-specific doctrine lives in `.agents/context/*.md` capsules — load only what the ROUTER points to.
- `.agents/workflows/*.md` carries longer or risky procedures (`/learn`, `/retro`, TDD).
- Adapter files (`CLAUDE.md`, `GEMINI.md`, etc.) are thin — they restate the load order, never duplicate this contract.
- In a conflict, `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (this file) — implicit, never skip.
2. `.agents/ROUTER.md` — identify the task family, pick the minimum context to load.
3. the capsule the router points to (if any).
4. the files directly touched by the request.
5. additional documentation only if the router points to it.

Never load large documents "just in case". Use progressive disclosure.

## Project

<2–4 lines an agent cannot deduce from the code: domain, deployment target, stage (alpha/beta/prod), any unusual architectural choice.>

## Essential commands

```bash
<run dev>                 # local dev server
<typecheck>               # type checker
<lint>                    # linter
<test>                    # unit tests
<format>                  # formatter — run before every commit
<build>                   # production build
<smoke>                   # smoke / integration check
```

## Critical zones

Files where mistakes are expensive. The detailed doctrine for each zone lives in its capsule under `.agents/context/`. The router points there.

| File or zone | Capsule (load on edit) | Risk level |
|---|---|---|
| `<path/to/critical-file.ts>` | `.agents/context/<domain>.md` | CRITICAL |
| `<path/to/another.ts>` | `.agents/context/<domain>.md` | HIGH |

## Minimal validation matrix

For each kind of change, the minimum command(s) the agent must run before declaring a task done.

| Change family | Validation minimum |
|---|---|
| UI / surface change | `<format>`, `<lint>`, `<typecheck>`, targeted test if behaviour changed |
| Business logic | `<typecheck>` + targeted tests |
| Data layer / mutations | `<typecheck>` + targeted tests + smoke if cross-device behaviour involved |
| Runtime / config / env | `<typecheck>` + smoke or integration command |
| Agent memory (`AGENTS.md`, `.agents/**`, `WORKFLOW.md`) | validate links + (at L) `validate_agent_context.*` |
| Documentation only | check internal links resolve |

If a change spans multiple families, run the union.

## Risk rail (declare after every task)

Every PR — and every direct commit on `main` if applicable — must declare a rail in its body:

- **Rail: green | amber | red**

| Rail | Meaning |
|---|---|
| `green` | small/local; no critical zone touched; no `.github/CODEOWNERS` path (at L) |
| `amber` | behavioural or transverse; short human review or owner approval |
| `red` | critical path or production risk; full review mandatory |

Detail and the formal PR-body template: `.github/pull_request_template.md`. At L, a CI gate enforces this.

## Learning loop

- After every release of a cycle: invoke `/retro` (see `.agents/workflows/retro.md`).
- For everything else worth capturing (incident, recurring friction, refactor, blocked candidate): invoke `/learn` (see `.agents/workflows/learning-loop.md`).
- Hard constraint in both: **one action retained**, lands in the most actionable artefact, validated with the user before diffusion.

## Skills and workflows

<list project-specific skills here as they emerge. Examples:>

| Skill / workflow | Trigger | Role |
|---|---|---|
| `<skill-name>` | <when to invoke> | <what it does> |
| `/retro [YYYY-MM-DD]` | within 24h after a release | post-release retrospective + diffusion |
| `/learn <scope>` | incident, friction, refactor, blocked candidate | learning loop outside releases |

## Reference documents

| Document | Usage |
|---|---|
| `WORKFLOW.md` | branches, commits, PRs, DoD |
| `STATUS_APP.md` | current state, recent decisions, release checklist |
| `CLAUDE.md` | Claude adapter (if applicable) |
| `.agents/ROUTER.md` | task family → context routing |
| `.agents/context/*.md` | per-domain critical doctrine |

## Promotion criterion to size L

Adopt L when **two or more** are true:

- This `AGENTS.md` has grown past ~250 lines and is hard to navigate.
- The same procedure has been re-explained to agents three or more times → write a pattern.
- A retro produced a procedural lesson that doesn't fit any existing file → consider a project-specific skill.
- You have two or more agents rotating on the codebase and need machine-enforced consistency (rail-guard CI, meta-validator).
- A critical zone has produced one major incident → pattern + ADR + maybe a project-specific skill.

When promoting: don't rename anything. Add `.agents/patterns/INDEX.md` + patterns, `.agents/rules/`, project skills, `docs/adr/`, `scripts/validate_agent_context.*` (meta-validator), `scripts/check_pr_rail_consistency.*` (rail guard), `.github/CODEOWNERS`, and **both** CI workflows: `agent-context.yml` (non-blocking signal on harness changes) and `pr-rail-guard.yml` (blocking gate on PR risk rail). Promoting the validator without the rail guard installs only half the L enforcement.
