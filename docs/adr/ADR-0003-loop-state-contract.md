# ADR-0003: Loop spec/state contract and L+ hardening (four volets)

- Status: accepted
- Date: 2026-07-08

## Context

ADR-0002 introduced L+ and `.agents/workflows/loop.md`, but step 6 only says "write the loop's assumptions and outcome to its state file" without defining where that file lives, what it must contain, or when a run is complete. Headless and manual loops therefore risk silent failure: fluent output with no durable state, or verification failures that never reach the next iteration.

Separately, loop-engineering practice (M0, maker-checker, permission floors) identified four gaps in the dogfooded L+ profile: no on-disk goal spec, no state contract, no deterministic permission floor in `settings.json`, and no agent-agnostic tier vocabulary for multi-model routing.

## Decision

We harden L+ in **four volets** (landed across follow-up PRs; this ADR is the anchor):

1. **Goal spec + state file (this change).** Every activated `/loop` owns `docs/loops/<slug>/SPEC.md` (goal, done-when, never-touch, stop-if, budget, permission level) and `docs/loops/<slug>/STATE.md` (operational memory). A run is **not complete** until STATE is updated; verification failures are **written** to STATE, not hidden.
2. **Deterministic permissions (follow-up).** `.claude/settings.json` gains an `allow`/`deny` floor; prose alone is insufficient for unattended runs.
3. **Permission ladder inside L+ (this change).** Six levels (read-only → automated low-risk writes); new loops start at ≤ 2; promotion after three stable runs, recorded in SPEC.
4. **Tiered-model pattern (follow-up).** Doctrine speaks in capability tiers (`top`/`mid`/`low`/`cross-family`), not concrete model names; runtime resolution cached locally.

Loops remain opt-in, ADR-gated, and subject to the three hard brakes from ADR-0002. Nothing here makes unattended autonomy the default.

## Consequences

Positive:

- Loops survive CI checkout and session boundaries; the Ralph-Wiggum failure mode (re-planning finished steps) is blocked by STATE + Do Not Repeat.
- Downstream L+ templates ship a copyable spec/state contract, not tribal knowledge.

Negative:

- More files per loop (`docs/loops/<slug>/`); mitigated by STATE ≤ 60 lines and reports in `reports/`.
- Permission ladder at six levels is doctrine ahead of dogfood; trim via `/learn` if friction shows it is unused.

## Notes

- Complements ADR-0002; does not supersede it.
- Scheduled-run policy lives in `loop.md` but headless `schedule:` remains manual-dispatch until brakes are exercised in production.
