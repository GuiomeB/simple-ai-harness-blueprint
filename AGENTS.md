# simple-ai-harness-blueprint — Agent Contract

> Doctrine: v5 (5 règles Karpathy + M0) — appliquée 2026-06-24

## Doctrine — the 5 Karpathy rules

Before any action on this repo, **every agent** (Claude Code, Codex CLI, Cursor, Antigravity, Copilot, …) applies these rules in order. They override convenience and any other rule in this file when conflicts arise. They are *posture*; the verification mechanism is **M0** (below).

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

The 5 rules are posture; **M0 is the mechanism every task inherits.** Before acting, state a **verifiable success criterion**, then loop until it holds. Operational form:

- **Trigger** — what starts the work.
- **Stop criterion** — the verifiable signal it's done (red test → green, lint clean, smoke passes).
- **Validation** — the minimum commands from §Minimal validation matrix.
- **Budget** — a ceiling on time / iterations / tokens.
- **Stop / no-progress** — if the criterion isn't converging, stop and surface the blocker (rule 1) instead of looping blindly.

The validation matrix, the Definition of Done (`WORKFLOW.md`), `/tdd-loop`, and — at L+ only — `/loop` all inherit from M0.

## Role of this file

- `AGENTS.md` is the canonical contract for all agents. Codex CLI reads it natively; Claude Code reads it via `CLAUDE.md` adapter.
- Domain-specific doctrine lives in `.agents/context/*.md` capsules — load only what the ROUTER points to.
- `.agents/patterns/*.md` carries short, copyable procedures keyed to pivot files in the codebase.
- `.agents/rules/*.md` carries narrow technical conventions (test signatures, smoke script contracts, etc.).
- `.agents/workflows/*.md` carries longer or risky procedures (`/learn`, `/retro`, TDD).
- `.agents/skills/<name>/SKILL.md` carries project-specific Claude skills (Anthropic format).
- Adapter files (`CLAUDE.md`, `GEMINI.md`, etc.) are thin — they restate the load order, never duplicate this contract.
- In a conflict, `AGENTS.md` wins.

## Context loading order (every new request)

1. `AGENTS.md` (this file) — implicit, never skip.
2. `.agents/ROUTER.md` — identify the task family, pick the minimum context to load.
3. the capsule and/or pattern the router points to (if any).
4. the files directly touched by the request.
5. additional documentation only if the router points to it.

Never load large documents "just in case". Never load more than 3 capsules + patterns simultaneously — if it feels like more, the task is over-scoped, split it.

## Project

Open-source template repo (`simple-ai-harness-blueprint`) providing a copyable AI-collaboration scaffold — `AGENTS.md` + `CLAUDE.md` + `.agents/` + meta-validator + risk-rail CI — for projects where AI agents and humans collaborate via strict PR workflow on GitHub. Bootstrap stage: no application code yet; current artefacts are documentation, templates, and CI scaffolding. Active agents: Claude Code (primary), Codex CLI (occasional).

## Essential commands

```bash
<run dev>                 # local dev server (n/a at bootstrap stage)
<typecheck>               # type checker (n/a at bootstrap stage)
<lint>                    # linter (n/a at bootstrap stage)
<test>                    # unit tests (n/a at bootstrap stage)
<format>                  # formatter — run before every commit (n/a at bootstrap stage)
<build>                   # production build (n/a at bootstrap stage)
<smoke>                   # smoke / integration check (n/a at bootstrap stage)
python scripts/validate_agent_context.py    # meta-validator (this harness)
```

Replace each `<placeholder>` once the corresponding tool is wired in. Until then, only the validator is operational.

## Critical zones

Files where mistakes are expensive. At bootstrap stage the only critical zones are the harness itself: every contract / template change affects every downstream user of the blueprint.

| File or zone | Capsule | Pattern | Project skill |
|---|---|---|---|
| `AGENTS.md`, `.agents/**`, `WORKFLOW.md` | (no capsule — meta) | `.agents/patterns/change-critical-zone.md` | — |
| `scripts/validate_agent_context.py` | (no capsule — meta) | `.agents/patterns/change-critical-zone.md` | — |
| `.github/workflows/pr-rail-guard.yml`, `scripts/check_pr_rail_consistency.py` | (no capsule — meta) | `.agents/patterns/change-critical-zone.md` | — |
| `<path/to/future-critical-file>` | `.agents/context/<domain>.md` | `.agents/patterns/change-critical-zone.md` | `<project-skill>` if any |

The full list of critical paths for CI gating lives in `.github/CODEOWNERS`.

## Minimal validation matrix

For each kind of change, the minimum command(s) the agent must run before declaring a task done.

| Change family | Validation minimum |
|---|---|
| UI / surface change | `<format>`, `<lint>`, `<typecheck>`, targeted test if behaviour changed |
| Business logic | `<typecheck>` + targeted tests |
| Data layer / mutations | `<typecheck>` + targeted tests + `<smoke>` if cross-device behaviour involved |
| Runtime / config / env | `<typecheck>` + `<smoke>` or integration command |
| Agent memory (`AGENTS.md`, `.agents/**`, `WORKFLOW.md`) | `python scripts/validate_agent_context.py` |
| Template / blueprint files (this is a template repo) | `python scripts/validate_agent_context.py`, plus a dry-run copy of the touched template into a scratch repo if the surface is non-trivial |
| Documentation only | check internal links resolve |

If a change spans multiple families, run the union.

## Risk rail (declare in every PR)

Every PR declares a rail in its body — see `.github/pull_request_template.md`.

- **Rail: green | amber | red**

Machine enforcement: the CI job `pr-rail-guard` (workflow `.github/workflows/pr-rail-guard.yml`, script `scripts/check_pr_rail_consistency.py`) fails any PR declared `green` that touches a path listed in `.github/CODEOWNERS`. Reclassify to `amber` or `red` and re-push. No `--no-verify`-style escapes.

## Learning loop

- After every release of a cycle: invoke `/retro` (see `.agents/workflows/retro.md`).
- For everything else worth capturing (incident, recurring friction, refactor, blocked candidate): invoke `/learn` (see `.agents/workflows/learning-loop.md`).
- Hard constraint in both: **one action retained**, lands in the most actionable artefact, validated with the user before diffusion.
- After every diffusion that touches `.agents/**` or `AGENTS.md`: re-run `python scripts/validate_agent_context.py`.

## Skills and workflows

| Skill / workflow | Trigger | Role |
|---|---|---|
| `<project-skill-name>` (`.agents/skills/<name>/SKILL.md`) | <when this project skill should be invoked> | <what it does> |
| `/retro [YYYY-MM-DD]` | within 24h after a release | post-release retrospective + diffusion |
| `/learn <scope>` | incident, friction, refactor, blocked candidate | learning loop outside releases |
| `/tdd-loop` (workflow) | new business logic or new mutation | RED → GREEN → REFACTOR with strict RED-state criteria |
| `/loop` (workflow, L+ only) | an explicitly activated, ADR-gated autonomous run | unit-of-work loop with the three hard brakes + reviewer verification |

## Execution primitives (subagents, glob-rules, bounded autonomy)

Deterministic helpers that make L safe to run with fewer babysitters. The *concept* is universal and lives here; the *Claude wiring* lives under `.claude/` — a thin runtime adapter, the same way `CLAUDE.md` is a thin doc adapter. Other agents wire the equivalent in their own runtime.

- **`.claude/` vs `.agents/`.** `.agents/**` is agent-agnostic doctrine (router, capsules, patterns, rules, workflows). `.claude/**` is Claude-Code-specific runtime (subagents now; hooks/settings at L+). Never put doctrine in `.claude/`; never put Claude runtime in `.agents/`.
- **Reviewer subagent** (`.claude/agents/harness-reviewer.md`): read-only, narrow `tools:` allowlist, `model: sonnet`. The coder is not the judge. It is the *executable instance* of `.agents/patterns/review-parallel-ticket.md` — invoke it before a PR that touches the harness. Cross-ref, not a copy: the pattern holds the doctrine.
- **Glob-scoped rules**: rules under `.agents/rules/` may carry `globs:` frontmatter to auto-load (zero token cost otherwise) when a matching file is edited. Complementary to the ROUTER, never a replacement — keep both in sync.
- **Bounded-autonomy doctrine (doctrine only at L).** If a bounded loop is ever run, it MUST carry hard brakes: a budget (iterations / tokens / time), an explicit stop criterion (M0), no-progress detection, and reviewer-subagent verification. **Activation of unattended loops is reserved to the L+ profile** (`/loop`, opt-in, ADR-gated). At L the default stays conservative: clarify, small diff, local validation.

## Autonomy profile (L+ — opt-in, ADR-gated; this repo dogfoods it)

**L+ is not a bigger L. It is a capability profile**: the same L harness, *plus* the wiring to run bounded loops unattended. It is opt-in, gated by `docs/adr/ADR-0002-lplus-autonomous-execution-profile.md`, and **never the default**. By default this repo stays conservative: clarify, small diff, local validation.

Promote to L+ only when **all five** are true: repeated loops with a verifiable goal · real unattended execution · parallel subagents or worktrees · a CI / headless runner exists · budgets and stop-conditions are genuinely needed. None of these → stay at L.

What L+ adds over L (all present and dogfooded here):

- `.agents/workflows/loop.md` — the `/loop` unit-of-work with the **three hard brakes** (budget · no-progress detection · kill-switch) and `harness-reviewer` verification.
- `.claude/settings.json` + `.claude/hooks/gate_git_push.sh` — push-to-main *defer* gate + denied-permission log (the formatter hook is left to downstream code repos).
- `.github/workflows/headless-loop.yml` — the headless runner, **manual-dispatch only** until the brakes are exercised.

**Hard rule:** a loop without all three brakes is forbidden. The unattended clause of Karpathy rule 1 applies *only* inside an activated `/loop`.

## Reference documents

| Document | Usage |
|---|---|
| `WORKFLOW.md` | branches, commits, PRs, DoD, CI gates |
| `STATUS_APP.md` | current state, recent decisions, release checklist |
| `CLAUDE.md` | Claude adapter (Claude Code is the primary agent) |
| `.agents/ROUTER.md` | task family → context routing |
| `.agents/context/*.md` | per-domain critical doctrine |
| `.agents/patterns/INDEX.md` | registry of patterns ↔ pivot files |
| `.agents/workflows/loop.md` | the L+ `/loop` profile (opt-in) |
| `docs/adr/` | Architecture Decision Records |
| `docs/retro/` | historical record of post-release retrospectives |
| `docs/learn/` | audit trail of `/learn` events |

## Maintenance and evolution

**L is the end of the general additive ladder; L+ is a specialised, opt-in autonomy profile on top of it (ADR-0002) — not a sixth size.** The system maintains itself via:

- `/retro` after every release
- `/learn` after every meaningful friction or incident
- `python scripts/validate_agent_context.py` after every `.agents/**` edit
- the non-blocking CI job `agent-context` for ambient drift detection

Further extension means: more patterns under `.agents/patterns/` (each ≤ 120 lines, keyed to pivot files, registered in `patterns/INDEX.md`), more rules under `.agents/rules/`, more project-specific skills under `.agents/skills/`. Not new top-level files. Not more capsules without a `ROUTER.md` entry. Not more files outside the validator's scope.

If something doesn't fit any of these slots, it's probably an ADR (`docs/adr/`) or a runbook entry — not a blueprint artefact.
