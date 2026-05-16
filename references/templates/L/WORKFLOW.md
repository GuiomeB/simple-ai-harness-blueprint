# Workflow — <Project Name>

Source of truth for contribution discipline. Universal across humans and agents.

## 1. Branch & commit strategy

- Default branch: `main`.
- Feature work: `feature/<short-slug>` from `main`.
- Fix work: `fix/<short-slug>` from `main`.
- Release branches (when applicable): `release/cycle-YYYY-MM-DD`.
- Commit messages: imperative, ≤ 72 characters in the subject line.

## 2. Split-work threshold

If the estimated diff exceeds **~500 net lines** *or* spans **more than 2 independent functional axes**, **force a split** at planning. Don't ship monsters.

- Document the sub-tasks in your tracker or in the PR description.
- Reference a previously merged file as a template if applicable.
- If split is decided mid-flight, stop at the next reviewable milestone, commit, push as draft, and open child tasks **before** continuing.

## 3. Pull Requests

- Every PR targets `main`.
- 1 PR = a coherent functional scope.
- Every PR declares a **risk rail** in its body — see `.github/pull_request_template.md`.
- Don't merge with a failing CI.

## 4. Definition of Done (per task / per PR)

- [ ] All four Karpathy rules satisfied (`AGENTS.md §Doctrine`).
- [ ] `<format>` run; no formatter drift.
- [ ] `<typecheck>` passes.
- [ ] `<test>` passes (or new tests added if behaviour changed).
- [ ] `<smoke>` or integration command run if a critical zone or runtime is touched.
- [ ] Risk rail declared in the PR body (`green` / `amber` / `red`).
- [ ] If the PR touches `AGENTS.md`, `.agents/**`, or `WORKFLOW.md`: `python scripts/validate_agent_context.py` ran clean.
- [ ] If a friction recurred or a procedure emerged: `/learn` invoked.

## 5. Risk rail enforcement at L

The rail rule (`green` / `amber` / `red`) is **machine-enforced** at L:

- Source of truth for critical paths: `.github/CODEOWNERS`.
- CI gate: the job `pr-rail-guard` (or equivalent) fails any PR declared `green` that touches a CODEOWNERS path.
- The CI workflow `agent-context.yml` runs `validate_agent_context.py` on every change to `AGENTS.md`, `.agents/**`, or `WORKFLOW.md`. Non-blocking — produces a visible signal, not a hard gate.

Bypass discipline:

- No `--no-verify`-style escapes.
- No editing `CODEOWNERS` to lower a rail. If a path no longer warrants amber/red, write an ADR explaining the change first.

## 6. When to invoke `/retro` and `/learn`

- **`/retro <YYYY-MM-DD>`** — within 24h after every release of a cycle (GO or NO-GO). Workflow: `.agents/workflows/retro.md`.
- **`/learn <family> <slug>`** — incident, no-go release candidate, recurring friction, meaningful refactor. Workflow: `.agents/workflows/learning-loop.md`.

Hard constraint in both: **one action retained**, lands in the most actionable artefact, validated with the user before being diffused. Re-run the validator after every diffusion that touches the harness.

## 7. Architecture Decision Records

For any decision that:
- changes a load-bearing assumption,
- affects deployment topology, or
- introduces or removes a non-bypassable rule,

write an ADR under `docs/adr/ADR-<NNNN>-<slug>.md`. See `docs/adr/README.md` for the format.

## 8. Beyond L

The harness has no further size. Evolution = more patterns, more rules, more project-specific skills under `.agents/skills/`, more ADRs. Not new top-level files. If something doesn't fit, it's a runbook entry or an ADR — not a new blueprint artefact.
