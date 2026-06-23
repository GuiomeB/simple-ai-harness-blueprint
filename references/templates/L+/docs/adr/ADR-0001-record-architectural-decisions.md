# ADR-0001: Record architectural decisions

- Status: accepted
- Date: <YYYY-MM-DD>

## Context

This project is large enough that load-bearing decisions are taken regularly: which library to depend on, which write-path to adopt, how to handle auth, which deployment strategy to commit to. These decisions shape the codebase for months or years.

Without a record:

- The rationale evaporates within weeks. New contributors (human or agent) ask "why is it like this?" and nobody remembers.
- Decisions get re-litigated when someone arrives with fresh ideas, without the context of why earlier alternatives were rejected.
- Spike decisions (taken under uncertainty) silently become permanent.

The project already has:

- `AGENTS.md` as the universal agent contract,
- `.agents/context/*.md` capsules for per-domain doctrine,
- `.agents/patterns/*.md` for procedural patterns,
- `STATUS_APP.md` as the current state of the project.

None of these are the right home for "this is why we chose X over Y on date Z". That's an ADR.

## Decision

We will use Architecture Decision Records under `docs/adr/`, following the format documented in `docs/adr/README.md`. Any decision that changes a load-bearing assumption, affects multiple critical zones, introduces or removes a non-bypassable rule, or is taken under significant uncertainty must be recorded as an ADR.

ADRs are sequential, dated, append-only as a corpus, and immutable once `accepted` (except for clarifications and supersession links).

## Consequences

Positive:

- The rationale of major decisions survives turnover, agent rotation, and context loss between sessions.
- Spike decisions (`.agents/patterns/spike-with-revisit-thresholds.md`) have a natural home with revisit thresholds.
- Agents reading `AGENTS.md` can be pointed to a specific ADR for any doctrinal rule that traces back to a recorded decision.

Negative:

- ADR discipline requires a small amount of overhead at decision time. Not every decision deserves one, so judgment is needed.
- The ADR corpus can rot if old, superseded ADRs aren't clearly marked.
- ADRs are not a substitute for talking to people about decisions in real time. They're the *record*, not the *deliberation*.

## Notes

- The meta-validator `scripts/validate_agent_context.py` checks internal links in ADRs, catching dangling references to superseded ADRs or missing files.
- A starter `docs/adr/README.md` documents the format and the trigger criteria.
