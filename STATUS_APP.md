# simple-ai-harness-blueprint — STATUS APP (Source of Truth)

Date: 2026-05-15
Branch of reference: `main`
Last production deploy: `none yet` — bootstrap stage; no release cut yet.
Recent scope: initial scaffold of the size-L harness (AGENTS / CLAUDE / .agents / docs / scripts / .github).
Next milestone: open-source publication — fill the placeholders, write a README quickstart, add a license, tag `v0.1.0`.

---

## 1. Snapshot

- Runtime: n/a — documentation + templates only at this stage.
- Critical zones state: harness scaffold drafted; downstream-facing templates ship with placeholders.
- Active feature flags: none.
- Open architectural questions: license choice; whether the project ships a CLI / installer or stays copy-paste.

## 2. Progress (axes → state → evidence)

| Axis | State | Evidence |
|---|---|---|
| L-harness scaffold (AGENTS / CLAUDE / WORKFLOW / .agents / docs / scripts / .github) | DONE (initial bootstrap) | this repo |
| Meta-validator | DONE | `scripts/validate_agent_context.py` |
| Risk-rail CI gate | DONE | `.github/workflows/pr-rail-guard.yml`, `scripts/check_pr_rail_consistency.py` |
| Worked example capsule (`data-mutations.md`) | IN_PROGRESS | kept as pedagogical example; replace or delete once a real domain emerges |
| Project-specific Claude skill | IN_PROGRESS | template at `.agents/skills/example-project-skill/SKILL.md.template` |
| Application code / tooling commands | BLOCKED | no app code yet; `<run dev>`, `<typecheck>`, `<lint>`, `<test>`, `<format>`, `<build>`, `<smoke>` to be filled |
| README quickstart for downstream users | IN_PROGRESS | placeholder section in `README.md` |
| License | BLOCKED | TBD (MIT or Apache-2.0 likely) |

States:
- `DONE` — landed in `main` and validated in the target environment
- `IN_PROGRESS` — under active work
- `BLOCKED` — explicit blocker noted in the evidence column

## 3. Current release checklist

No release in flight. Reactivate this section when cutting `v0.1.0`.

- [ ] Scope merged on `main`
- [ ] `<typecheck>` + `<test>` + `<smoke>` green
- [ ] PR rail review done
- [ ] Release doc generated (if applicable)
- [ ] Preprod / staging validated
- [ ] Production deploy executed
- [ ] `/retro` invoked within 24h after deploy

## 4. Recent decisions

- 2026-05-15 — Bootstrap the repo directly at size L (not S → M → L progression) because the project's *purpose* is to ship the L harness as a reference; the audience needs to see the full system. See `docs/adr/ADR-0001-record-architectural-decisions.md` for the decision to use ADRs at all.

## 5. Known debt / signals to watch

- Every `<placeholder>` in `AGENTS.md §Essential commands` and the validation matrix is unresolved by design — they become technical debt the moment app code lands without them being filled.
- The worked example capsule (`.agents/context/data-mutations.md`) is pedagogical, not project-specific. Decide its fate before publishing: delete (and remove the matching ROUTER row), generalize, or keep with an explicit "example" disclaimer.
- `.github/CODEOWNERS` owners are placeholder `@<owner>` strings. Replace with a real GitHub handle or team before relying on branch protection.

## 6. Active references

- `WORKFLOW.md` (process, branches, CI)
- `AGENTS.md` (universal agent contract)
- `CLAUDE.md` (Claude adapter)
- `.agents/ROUTER.md` (task routing)
- `docs/adr/ADR-0001-record-architectural-decisions.md`
