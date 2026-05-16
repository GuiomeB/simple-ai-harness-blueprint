# Workflow — <Project Name>

Source of truth for contribution discipline. Universal across humans and agents.

## 1. Branch & commit strategy

- Default branch: `main`.
- Feature work: `feature/<short-slug>` from `main`.
- Fix work: `fix/<short-slug>` from `main`.
- Release branches (when applicable): `release/cycle-YYYY-MM-DD`.
- Commit messages: imperative, ≤ 72 characters in the subject line. Body optional but encouraged for non-trivial changes.

## 2. Split-work threshold (don't ship monsters)

Before starting implementation, if the estimated diff exceeds **~500 net lines** *or* spans **more than 2 independent functional axes** (e.g. backend + frontend + ops in the same change), **force a split** at the planning stage — not mid-implementation.

- Document the sub-tasks (in your tracker, in comments, or in a short note in the PR description).
- Reference a template if one exists (a previously merged file that follows the same pattern).
- If a split is decided mid-flight, stop at the next reviewable milestone, commit, push as draft, and open the child tasks **before** continuing.

Why: parallel review is faster, parallel agents can collaborate, and rollbacks stay surgical. A 1500-line PR will hide its own bugs.

## 3. Pull Requests

- Every PR targets `main`.
- 1 PR = a coherent functional scope (not necessarily 1 ticket).
- Every PR must declare a **risk rail** in its body — see `.github/pull_request_template.md`.
- Do not merge a PR with a failing CI.

## 4. Definition of Done (per task / per PR)

- [ ] All four Karpathy rules satisfied (`AGENTS.md §Doctrine`).
- [ ] `<format>` run; no formatter drift.
- [ ] `<typecheck>` passes.
- [ ] `<test>` passes (or new tests added if behaviour changed).
- [ ] Smoke or integration command run if a critical zone or runtime is touched.
- [ ] Risk rail declared in the PR body (`green` / `amber` / `red`).
- [ ] If the PR touches `AGENTS.md`, `.agents/**`, or `WORKFLOW.md`, the link/path consistency has been re-checked.
- [ ] If a friction recurred or a procedure emerged, `/learn` has been invoked.

## 5. Risk rail enforcement at M

The rail rule (`green` / `amber` / `red`) is declared in the PR body via `.github/pull_request_template.md`. At M, the rail is **human-enforced**: you read the rail, you decide review depth. Use the rail vocabulary consistently — it transitions cleanly to machine enforcement at L (see promotion section).

## 6. When to invoke `/retro` and `/learn`

- **`/retro`** — within 24h after every release of a cycle (GO or NO-GO). Workflow: `.agents/workflows/retro.md`.
- **`/learn`** — incident, no-go release candidate, recurring friction, meaningful refactor. Workflow: `.agents/workflows/learning-loop.md`.

Hard constraint in both: **one action retained**, lands in the most actionable artefact (`AGENTS.md`, `WORKFLOW.md`, a capsule, a workflow, or `STATUS_APP.md`), and is validated with the user before being diffused.

## 7. Promotion to L

Adopt L when criteria in `AGENTS.md §Promotion criterion to size L` are met. Additions at L:

- `.agents/patterns/INDEX.md` + concrete patterns
- `.agents/rules/` for narrow technical conventions
- `.agents/skills/<project-skill>/SKILL.md` for project-specific Claude skills
- `docs/adr/` for Architecture Decision Records
- `scripts/validate_agent_context.*` (meta-validator) **and** `scripts/check_pr_rail_consistency.*` (rail guard) — install both, not just one
- `.github/CODEOWNERS` + `.github/workflows/agent-context.yml` (non-blocking signal) + `.github/workflows/pr-rail-guard.yml` (blocking gate on PR rail mismatch)

No filename changes between M and L. Only additions.
