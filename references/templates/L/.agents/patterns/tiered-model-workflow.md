# Pattern — Tiered model workflow

**Pivot trigger:** any activated `/loop` or multi-step run that routes work across
roles (plan → implement → test → review), or explicit tiered handoffs.

**Shape:** execution pattern. Cost control + cross-family review without
hardcoding model names in doctrine.

**When to use:** repeated loops with enough volume that a single top-tier model
for every step is wasteful. **When not to:** one-off tasks, single-file edits, or
only one model available.

---

## Principle

Expensive reasoning at the **ends** (plan, final review). High-volume trial-and-error
in the **middle**. A **cross-family** reviewer catches blind spots the worker's
family shares. Doctrine names **tiers only** — never concrete model IDs.

## Role → tier (doctrine — no model names here)

| Role | Tier |
|---|---|
| Architect / planner | `top` |
| Implementation / build-fix loop | `mid` |
| Tests, boilerplate, fixtures | `low` |
| Reviewer (read-only) | `top` + `cross-family` |

## Tier discovery (before every tiered run)

1. If `_local/MODEL_TIERS.md` exists, is **< 30 days** old, and matches the
   current runtime → use it.
2. Else enumerate models **actually available in this runtime** (do not assume
   docs are current):
   - Claude Code — `/model` selector + `model:` on subagent frontmatter
   - Codex CLI — `codex` config / model list
   - Cursor — subagent model slugs offered in the Task tool
   - Gemini CLI — provider model list
3. Classify each candidate into `top` / `mid` / `low` by **observable** cost and
   reasoning-vs-execution positioning in that provider's lineup. `cross-family` =
   any model from a **different provider** than the main worker; if none → record
   `cross-family: none` and flag degraded cross-review.
4. Write resolution to `_local/MODEL_TIERS.md` (gitignored — same status as
   `CI_RULEBOOK.md`). Template:

   ```markdown
   # Model tier resolution
   - Date: <YYYY-MM-DD>
   - Runtime: <claude-code | codex | cursor | gemini | …>
   | Tier | Model |
   |---|---|
   | top | … |
   | mid | … |
   | low | … |
   | cross-family | … or none |
   - Rejected: …
   ```

   Two plausible `top` candidates → ask the human (Karpathy rule 1); do not guess.

## Definition of Ready (before handoff to a lower tier)

Handoff package must include:

- Verifiable goal (from `docs/loops/<slug>/SPEC.md` if in a loop)
- Files in scope
- Constraints and **Never touch**
- Validation command(s)
- Stop criterion

Incomplete handoff → do not route to a cheaper tier.

## Shared run log

Each tier updates `docs/loops/<slug>/STATE.md` (see `.agents/workflows/loop.md`)
with what it did and which tier resolution it used (`§Last Run`).

## Reusability

Reuse this pattern for any loop that fans out roles. Write a **new** pattern only
when the handoff shape differs materially (e.g. research fan-out vs code loop).
After the first real multi-tier run, invoke `/learn` and amend if friction appears.
