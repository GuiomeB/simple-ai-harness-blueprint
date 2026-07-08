# simple-ai-harness-blueprint — STATUS APP (Source of Truth)

Date: 2026-07-04
Branch of reference: `main`
Last production deploy: n/a — template/skill repo; "production" = published on GitHub (`GuiomeB/simple-ai-harness-blueprint`, MIT).
Recent scope: doctrine v5 (5 Karpathy rules + M0), L execution primitives, L+ autonomy profile (PR #2, 2026-06-24) ; doctrine version stamp + fleet audit + release checklist (PR courant).
Next milestone: tag `doctrine-v5`, then keep the fleet green via `scripts/audit_fleet.py`.

---

## 1. Snapshot

- Runtime: n/a — documentation + templates + two Python scripts (validator, fleet audit).
- Critical zones state: harness contract stable in v5; templates S/M/L/L+ aligned (stamp included).
- Active feature flags: none.
- Open architectural questions: none blocking. Distribution of the claude.ai skill copy is manual (re-upload after each doctrine release — see WORKFLOW §8).

## 2. Progress (axes → state → evidence)

| Axis | State | Evidence |
|---|---|---|
| L-harness scaffold (AGENTS / CLAUDE / WORKFLOW / .agents / docs / scripts / .github) | DONE | this repo |
| Meta-validator | DONE | `scripts/validate_agent_context.py` |
| Risk-rail CI gate | DONE | `.github/workflows/pr-rail-guard.yml`, `scripts/check_pr_rail_consistency.py` |
| Doctrine v5 (5 rules + M0) | DONE | PR #2 merged 2026-06-24 (`a16b203`) |
| L+ autonomy profile (dogfooded) | DONE | `docs/adr/ADR-0002-lplus-autonomous-execution-profile.md`, `.claude/hooks/`, `/loop` |
| Doctrine version stamp + fleet audit + release checklist | IN_PROGRESS | branch `feature/doctrine-versioning` — `scripts/audit_fleet.py`, WORKFLOW §8 |
| License | DONE | `LICENSE` (MIT) |
| Worked example capsule (`data-mutations.md`) | DONE | kept with explicit pedagogical role in the M templates |
| Application code / tooling commands | N/A | template repo by design; `<run dev>` etc. stay placeholders |

States: `DONE` — landed in `main` and validated · `IN_PROGRESS` — under active work · `N/A` — intentionally out of scope.

## 3. Current release checklist

Doctrine release in flight (versioning PR). Follow `WORKFLOW.md §8`:

- [x] Doctrine change merged on `main` (v5, 2026-06-24)
- [ ] Version stamp + audit + checklist PR merged
- [ ] STATUS_APP.md up to date (this file)
- [ ] Tag `doctrine-v5`
- [ ] claude.ai skill copy re-uploaded
- [ ] `python scripts/audit_fleet.py` — fleet green or explicitly frozen

## 4. Recent decisions

- 2026-07-04 — Add a greppable doctrine version stamp to every generated `AGENTS.md`, a read-only fleet audit script, and a doctrine release checklist (WORKFLOW §8). Motivated by fleet audit: ArrowZ and JSON_2_Sheets silently lagged on the 4-rule doctrine after the 2026-06-24 migration.
- 2026-06-24 — Doctrine v5: revise Karpathy rules (4→5), promote verification to a separate M0 mechanism; add L execution primitives and the opt-in, ADR-gated L+ autonomy profile (PR #2).
- 2026-05-15 — Bootstrap the repo directly at size L (see `docs/adr/ADR-0001-record-architectural-decisions.md`).

## 5. Known debt / signals to watch

- The claude.ai uploaded skill copy does not track this repo — it must be re-uploaded after every doctrine release (WORKFLOW §8 step 3). The `~/.codex/skills` symlink follows automatically.
- `.github/CODEOWNERS` owners remain placeholder `@<owner>` strings — replace before relying on branch protection.
- `docs/learn/` and `docs/retro/` are empty on this repo itself: the blueprint's own learning loop has not run yet. First real `/retro` due after the `doctrine-v5` tag.

## 6. Active references

- `WORKFLOW.md` (process, branches, CI, doctrine release checklist §8)
- `AGENTS.md` (universal agent contract — stamped v5)
- `CLAUDE.md` (Claude adapter)
- `scripts/audit_fleet.py` (fleet-wide doctrine audit)
- `docs/adr/` (ADR-0001 records, ADR-0002 L+ profile)
