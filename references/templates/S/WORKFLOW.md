# Workflow — <Project Name>

Source of truth for contribution discipline. Universal across humans and agents.

## 1. Branch & commit strategy

- Default branch: `main`.
- Feature work: `feature/<short-slug>` from `main`.
- Fix work: `fix/<short-slug>` from `main`.
- Commit messages: imperative, ≤ 72 characters in the subject line. Body optional.

If this project uses direct-to-main commits (acceptable at small scale):
- Each commit must still declare the risk rail (`AGENTS.md §Risk rail`).
- A commit on `main` that breaks the build is a `red` rail by default and must be reverted or hot-fixed immediately.

## 2. Definition of Done (per task)

A task is done when:

- [ ] All four Karpathy rules satisfied (`AGENTS.md §Doctrine`).
- [ ] `<format>` has been run; no formatter drift.
- [ ] `<typecheck>` passes.
- [ ] `<test>` passes (or new tests added if behaviour changed).
- [ ] Risk rail declared in the final message or PR body.
- [ ] If the task revealed a recurring friction, `/learn` has been invoked.

## 3. Risk rail enforcement at S

The rail rule (`green` / `amber` / `red`) is **declarative only** at this stage. See `AGENTS.md §Risk rail`. No CI gate enforces it yet.

Agents must self-declare. The user uses the rail to decide review effort. If the same agent repeatedly under-declares (`green` on changes that were actually `amber`), that's a friction worth a `/learn` entry.

## 4. When to invoke `/learn`

`/learn` is defined in `.agents/workflows/learning-loop.md`. Invoke it when:

- The same kind of mistake happens twice or more.
- An incident requires explanation post hoc.
- A meaningful refactor reveals a procedure worth capturing.
- A release / candidate is rejected or blocked.

Hard constraint: one action retained per `/learn`. It lands in the most actionable artefact (`AGENTS.md`, this file, or — at M+ — a capsule or pattern).

## 5. Promotion to M

When you adopt size M (see `AGENTS.md §Promotion criterion to size M`):

- Add `STATUS_APP.md`, `.agents/ROUTER.md`, capsules under `.agents/context/`.
- Add `.github/pull_request_template.md` if you've moved to a PR workflow.
- Add `.agents/workflows/retro.md` to formalize post-release retrospectives.
- Move domain-specific accretion out of `AGENTS.md` into capsules.

No filename changes. Only additions.
