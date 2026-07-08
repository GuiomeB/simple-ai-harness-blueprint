# Loop spec — fleet-audit

## Goal

Each harnessed repo under `~/Dev` is on doctrine v5 or explicitly frozen; no silent lag.

## Done when

- `python scripts/audit_fleet.py` completes successfully.
- Report written to `docs/loops/fleet-audit/reports/<YYYY-MM-DD>.md`.
- `STATE.md` updated with PASS/FAIL and any repos needing human review.
- Zero repos on `inconnue` or stale doctrine without a documented freeze.

## Never touch

- Repos under `~/Dev` (read-only scan via `audit_fleet.py` only).
- No edits, commits, or pushes in audited repos from this loop.

## Stop if

- `audit_fleet.py` exits with error.
- Wall-clock exceeds 15 minutes.

## Budget

- 1 iteration per manual run; weekly cadence (manual).
- Tokens: minimal (report + STATE only).

## Permission level

2 — read fleet + draft reports under `docs/loops/fleet-audit/`.
