# ADR-0004: Stop gate blocks on validator errors only

- Status: accepted
- Date: 2026-09-18

## Context

The L+ Stop hook (`.claude/hooks/verify_on_stop.sh`) runs the meta-validator whenever harness files were edited in the turn and blocks the agent from ending its turn on any non-zero exit. The validator's own contract has always distinguished exit `1` (warnings: missing optional pieces) from exit `2` (errors: broken links, orphan patterns, missing capsules). Until now no warning-producing check fired on this repo, so the two behaviours never diverged.

The invariant-enforcement change adds a size-budget check that mirrors `SKILL.md §File size budgets`: a file past its soft target warns, past its hard ceiling errors. This repo's `AGENTS.md` sits above its soft target, so the validator now legitimately exits `1`. Left as is, the Stop hook would block every turn on an informational signal, which is the "validator noise" failure mode `references/health-metrics.md §10` warns about. The alternative, trimming `AGENTS.md` under 150 lines inside the same PR, would hide the signal the check exists to surface.

## Decision

The Stop gate blocks only on validator exit code `2` (errors). Exit code `1` (warnings) passes through and stays visible in the validator output, `STATUS_APP.md §Known debt`, and the non-blocking `agent-context` CI job. Soft targets remain advisory; hard ceilings remain blocking. The same split ships in `references/templates/L+/.claude/hooks/verify_on_stop.sh`.

## Consequences

- The warn / error semantics are now identical in the validator, the Stop hook, and CI. One contract, three consumers.
- A soft-target overshoot is a tracked debt item, not a turn blocker. The `AGENTS.md` overshoot is logged in `STATUS_APP.md` with an extraction candidate.
- Warnings can accumulate silently if nobody reads them. Mitigation: `references/health-metrics.md §10` and §11 make validator noise and edit volume explicit review triggers.
- Anyone who wants a zero-warning gate can lower the threshold in the hook to `-ge 1`; the change is one character and local to `.claude/`.
