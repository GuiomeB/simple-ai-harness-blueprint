# simple-ai-harness-blueprint — STATUS APP (Source of Truth)

Date: 2026-07-08
Branch of reference: `main`
Last production deploy: n/a — template/skill repo; "production" = published on GitHub (`GuiomeB/simple-ai-harness-blueprint`, MIT).
Recent scope: L+ hardening (ADR-0003 loop spec/state, deterministic permissions, tiered-model pattern) ; first dogfood loop `fleet-audit`.
Next milestone: merge L+ hardening PR stack; tag `doctrine-v5`; fleet lag resolution on flagged repos.

---

## 1. Snapshot

- Runtime: n/a — documentation + templates + Python scripts (validator, fleet audit, rail guard).
- Critical zones state: harness contract stable in v5; L+ profile extended (ADR-0003).
- Active feature flags: none.
- Open architectural questions: none blocking. Distribution of the claude.ai skill copy is manual (re-upload after each doctrine release — see WORKFLOW §8).

## 2. Progress (axes → state → evidence)

| Axis | State | Evidence |
|---|---|---|
| L-harness scaffold (AGENTS / CLAUDE / WORKFLOW / .agents / docs / scripts / .github) | DONE | this repo |
| Meta-validator | DONE | `scripts/validate_agent_context.py` |
| Risk-rail CI gate | DONE | `.github/workflows/pr-rail-guard.yml`, `scripts/check_pr_rail_consistency.py` |
| Doctrine v5 (5 rules + M0) | DONE | PR #2 merged 2026-06-24 (`a16b203`) |
| L+ autonomy profile (dogfooded) | DONE | ADR-0002, `.claude/hooks/`, `/loop` |
| L+ loop spec/state contract (ADR-0003) | DONE | `docs/adr/ADR-0003-loop-state-contract.md`, `loop.md` |
| Doctrine version stamp + fleet audit + release checklist | IN_PROGRESS | `scripts/audit_fleet.py`, WORKFLOW §8 |
| Première boucle L+ dogfoodée (fleet-audit) | DONE | `docs/loops/fleet-audit/` |
| License | DONE | `LICENSE` (MIT) |
| Worked example capsule (`data-mutations.md`) | DONE | kept with explicit pedagogical role in the M templates |
| Application code / tooling commands | N/A | template repo by design; `<run dev>` etc. stay placeholders |

States: `DONE` — landed in `main` and validated · `IN_PROGRESS` — under active work · `N/A` — intentionally out of scope.

## 3. Current release checklist

Doctrine release in flight. Follow `WORKFLOW.md §8`:

- [x] Doctrine change merged on `main` (v5, 2026-06-24)
- [ ] L+ hardening PR stack merged
- [ ] STATUS_APP.md up to date (this file)
- [ ] Tag `doctrine-v5`
- [ ] claude.ai skill copy re-uploaded
- [ ] Fleet green or explicitly frozen (`docs/loops/fleet-audit/reports/`)

## 4. Recent decisions

- 2026-07-08 — ADR-0003: mandatory SPEC/STATE for `/loop`; dogfood via manual `fleet-audit` loop (6 repos without doctrine stamp, 1 on v4 flagged).
- 2026-07-04 — Add doctrine version stamp, fleet audit script, release checklist (WORKFLOW §8).
- 2026-06-24 — Doctrine v5 + L+ autonomy profile (ADR-0002).
- 2026-05-15 — Bootstrap at size L (ADR-0001).

## 5. Known debt / signals to watch

- Fleet lag: see `docs/loops/fleet-audit/STATE.md §Needs Human Review`.
- The claude.ai uploaded skill copy does not track this repo — re-upload after doctrine release.
- `.github/CODEOWNERS` owners remain placeholder `@<owner>` strings.
- `docs/learn/` empty on this repo — first `/learn` from fleet-audit friction pending user validation.

## 6. Active references

- `WORKFLOW.md` (process, branches, CI, doctrine release checklist §8)
- `AGENTS.md` (universal agent contract — stamped v5)
- `CLAUDE.md` (Claude adapter)
- `scripts/audit_fleet.py` (fleet-wide doctrine audit)
- `docs/adr/` (ADR-0001, ADR-0002, ADR-0003)
- `docs/loops/fleet-audit/` (first L+ dogfood loop)
