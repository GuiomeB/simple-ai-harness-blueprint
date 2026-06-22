# Router — task family → context

Load the **minimum** context useful for the task at hand. Doesn't replace `AGENTS.md` (always implicit). Routes to the right capsule, pattern, workflow, skill, or rule.

## Loading order

1. `AGENTS.md` (implicit) — invariants, commands, validation matrix.
2. Identify the **task family** in the table below.
3. Load the **pivot capsule** + 0..N complements (capsule, pattern, rule).
4. Activate the skill or workflow indicated if the scope matches.
5. If the task reveals a recurring procedure → write or update a pattern. If a new technical convention emerges → add a rule.

> Per-zone validation lives in `AGENTS.md §Minimal validation matrix` — not duplicated here.

## Routing table

> The first row below is a **worked example** wired to `data-mutations.md` + `change-critical-zone.md`. This repo has no application code yet, so the row is kept as pedagogical reference for downstream users — replace or delete it once a real domain emerges in this project.

| Task family | Pivot capsule | Complements (capsule / pattern / rule) | Skill / workflow |
|---|---|---|---|
| Data mutations, optimistic UI, rollback, write-path consistency | `context/data-mutations.md` | `patterns/change-critical-zone.md` if a critical zone is touched | `/tdd-loop` for behaviour change |
| <Domain 2 — e.g. auth, sessions, identity> | `context/<domain-2>.md` | <list> | <skill / workflow> |
| <UI / design-system / component conventions> | `context/<ui-doctrine>.md` (if any) | `rules/<ui-rule>.md` if any | `<project-ui-skill>` if any |
| PR preparation / merge / risk rail | (no capsule) | `WORKFLOW.md`, `.github/pull_request_template.md`, `.github/CODEOWNERS` | none required |
| Release / deploy / candidate | (no capsule) | `STATUS_APP.md`, `WORKFLOW.md §release` | `/retro` after a release |
| Tests, fixtures, smoke scripts | `rules/test-conventions.md` | the test file of the domain, `.agents/workflows/tdd-loop.md` | none |
| Review another agent's PR | (no capsule) | `patterns/review-parallel-ticket.md`, the ticket / PR body, the capsule of the domain touched | none |
| Time-boxed architecture spike | (no capsule) | `patterns/spike-with-revisit-thresholds.md` | none |
| Retro, friction, refactor learning | (no capsule) | `STATUS_APP.md` if scope is project-wide | `/retro` (release) or `/learn <scope>` |
| Update the agent system itself (this file, capsules, patterns, `AGENTS.md`) | this file | `WORKFLOW.md`, `patterns/INDEX.md`, run `validate_agent_context.py` after | none |
| Edit an execution primitive (`.claude/agents/**`, glob-scoped rules, and at L+ hooks/settings) | (no capsule) | `AGENTS.md §Execution primitives`, run `validate_agent_context.py` after | `harness-reviewer` subagent |
| Run an activated autonomous loop (L+ only, ADR-gated) | (no capsule) | `AGENTS.md §Autonomy profile`, `.agents/workflows/loop.md`, `docs/adr/ADR-0002-lplus-autonomous-execution-profile.md` | `/loop` workflow |
| Edit a template file shipped to downstream users (`.agents/**`, `docs/adr/**`, `_local/**`) | (no capsule) | `patterns/change-critical-zone.md` (templates ARE the product here) | none |

Add one row per stable critical domain. Don't pre-create rows for files that don't exist yet.

## Choosing between adjacent families

- **Mutation client vs server write-path** → client-launched + propagated via API/RPC: client mutation. Server-owned (worker / edge): server write-path.
- **UI domain vs large refactor** → visual / component / tokens: UI. Logic debt or deeply nested file: refactor pattern.
- **Retro vs Learn** → release of a cycle: `/retro`. Everything else worth capturing: `/learn`.
- **Review-parallel-ticket vs ordinary PR review** → another agent owned the implementation: `patterns/review-parallel-ticket.md`. You wrote the code yourself: ordinary review, no pattern needed.

## Loading rules

- Don't load `STATUS_APP.md` by default for small local tasks. Reserve for release, runtime, auth, or roadmap topics.
- Patterns are loaded **in addition to** capsules, not in place of. A capsule defines doctrine; a pattern defines a procedure.
- Never load more than **3 capsules + patterns** simultaneously. If it feels like more, the task is over-scoped — split it (`WORKFLOW.md §2`).
- After updating the router or any `.agents/**` file, run `python scripts/validate_agent_context.py`.
