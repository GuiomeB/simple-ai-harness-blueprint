# Health metrics — diagnostic playbook

Extended diagnostic checklist for an existing harness. Load this file when auditing a repo that's been running on the blueprint for a while.

The base table lives in `SKILL.md §Health metrics`. This document expands it with: how to *detect* each symptom programmatically or by inspection, what *first fix* and *second fix* look like, when to escalate.

---

## How to use this document

Run a quarterly review:

1. Pick a quiet hour. Open the repo at `main`.
2. Walk through the symptoms below in order. For each, run the *detection* check.
3. If a symptom is present, decide: first fix now, second fix scheduled, or accept and document the exception in `_local/CI_RULEBOOK.md`.
4. Record the review as a `/learn refactor harness-review-<YYYY-MM-DD>` so the next audit can reference what changed.

Two or more active symptoms simultaneously → schedule a dedicated harness-rework sprint, not a one-off fix.

---

## Catalog

### 1. Agents read `AGENTS.md` then ignore the router

**Detect:** ask an agent to do a task in a routed domain. Does the agent open `.agents/ROUTER.md` and then the matching capsule? Or does it dive straight into source files?

**First fix:** the init rule is probably buried in `CLAUDE.md` (or equivalent adapter). Restate it at the top of `AGENTS.md §Role` so it survives careless edits to the adapter.

**Second fix:** consider promoting the init rule into the agent's IDE session-start hook when the IDE supports one.

---

### 2. Same friction reported 3+ times

**Detect:** grep `docs/learn/` for repeated keywords across recent files. Or check your own memory — has the same kind of mistake recurred?

**First fix:** run `/learn friction <slug>` *retroactively* on the most recent occurrence. The single retained action lands in the artefact most likely to prevent recurrence: a capsule, a rule, a pattern, or `AGENTS.md` itself.

**Second fix:** if the action keeps landing in the same file (e.g. always `AGENTS.md`), that file is acting as a catch-all. Promote: extract a capsule, a rule, or a pattern, and update the router.

---

### 3. `AGENTS.md` past its hard ceiling (300 lines) and growing

**Detect:** `wc -l AGENTS.md` and check the cap from `SKILL.md §File size budgets`.

**First fix:** identify which section grew. If it's "Critical zones" or "Validation matrix", that's expected — leave it. If it's a domain-specific section ("Auth rules", "Mutation patterns", …), extract it into `.agents/context/<domain>.md` and add a row in `.agents/ROUTER.md`.

**Second fix:** if multiple sections need extraction at once, consider that the project's complexity has grown faster than the harness. Schedule a structural review.

---

### 4. `.agents/` files contradict each other

**Detect:** run `python scripts/validate_agent_context.py`. Errors are usually broken links or orphan patterns. Read the warnings — they often expose dead capsules or unrouted patterns.

**First fix:** run a `/learn refactor harness-coherence-<date>` that decides one rule and removes the contradictory one. Update the validator's expectations if needed.

**Second fix:** if contradictions recur, run a second `/learn refactor harness-coherence-<date>` focused on the *system* itself, not just one rule. `/retro` stays reserved for post-release events — don't dilute it.

---

### 5. Token-heavy loads for trivial tasks

**Detect:** in an agent session, watch how many files get loaded before any code is written. If a UI tweak triggers loading STATUS_APP, two capsules, and three patterns — the router is too permissive.

**First fix:** tighten the routing rules. Add explicit "do not load by default" notes per file (e.g. "STATUS_APP.md is reserved for release / runtime / auth tasks").

**Second fix:** introduce per-task budgets in the router (e.g. "trivial UI: AGENTS.md + 1 capsule maximum").

---

### 6. A capsule hasn't been touched in 3+ months

**Detect:** `git log --since="3 months ago" -- .agents/context/<file>.md` returns nothing.

**First fix:** read the capsule and verify it's still accurate against current code. *Untouched is not the same as stale.* A capsule documenting a stable invariant should stay exactly as it is — that's the point. Decide between three outcomes:

- **Still accurate, still relevant** → leave it. Note the date of last review at the bottom if helpful.
- **Doctrine has migrated to `AGENTS.md` or another file** → delete the capsule and update `ROUTER.md`.
- **The zone is dead** (the code it documents was removed or rewritten beyond recognition) → delete with a short ADR explaining why the rationale no longer applies.

**Second fix:** if multiple capsules need this kind of review, schedule a harness audit using the quarterly review template at the bottom of this file. Don't process them one at a time across separate sessions.

---

### 7. A new agent (Cursor / Codex / Gemini / …) ignores rules everyone else follows

**Detect:** spot-check a PR from the new agent. Does it cite the 4 Karpathy rules? Did it declare a rail? Did it run the validation matrix?

**First fix:** verify the agent's entry file. Each agent reads a specific config (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`, …). If the agent reads an unusual file, either symlink `AGENTS.md` to its expected name or write a thin adapter pointing back to `AGENTS.md`.

**Second fix:** record the agent's setup in `_local/CI_RULEBOOK.md §Agent ecosystem` so future onboardings don't repeat the discovery.

---

### 8. Patterns INDEX has dangling references or orphan files

**Detect:** `python scripts/validate_agent_context.py` reports orphan patterns or ghost INDEX entries.

**First fix:** for each orphan on disk — add the row in INDEX. For each ghost in INDEX — either restore the file or remove the row.

**Second fix:** add a pre-commit hook that runs the validator on `.agents/patterns/` changes locally.

---

### 9. PRs routinely declare the wrong rail

**Detect:** in the last 10 merged PRs, count how many had `green` rails that should have been `amber` or `red`. If more than 2 — there's a discipline issue.

**First fix:** improve the `WORKFLOW.md §Risk rail` description with concrete examples drawn from the project. Generic descriptions don't internalize.

**Second fix:** lower CODEOWNERS coverage selectively — if a path is rarely critical, maybe it shouldn't be there. The CODEOWNERS list is doctrine, not paranoia.

---

### 10. The validator runs slow or produces noise

**Detect:** time the validator. If it takes more than 2 seconds on a repo with under 100 markdown files, something's wrong. If it warns on placeholders the project author intends — the validator is too strict.

**First fix:** verify placeholders use `<...>` syntax (the validator skips these by default). For real warnings the project wants to accept, document them in `_local/CI_RULEBOOK.md §Validator exceptions` with a revisit date.

**Second fix:** if validator warnings keep growing, the harness has rotted faster than it's being maintained. Run `/learn refactor harness-validator-noise-<YYYY-MM-DD>` to capture what stalled, land one action, and commit to running the validator weekly.

---

## Anti-patterns to avoid when "fixing" symptoms

- **Disabling the validator** because it warns on a known issue. The right move is to fix the issue or document the exception, never to silence the tool.
- **Adding more capsules to "cover" a friction** without first deciding whether a capsule (doctrine) or a pattern (procedure) is the right shape.
- **Editing `AGENTS.md §Promotion criterion`** to lower the bar for an upgrade you'd actually need. Promotion criteria are guardrails — if you're tempted to soften them, write an ADR explaining why.
- **Promoting the validator workflow to blocking** before it's been stable for a cycle. Codex's reminder: don't mix this signal with product CI until it's clean for at least one release cycle.

## Quarterly review template

Copy this into a `/learn refactor harness-review-<YYYY-MM-DD>` and complete it:

```markdown
# Harness review — <YYYY-MM-DD>

## Symptoms checked
- [ ] 1. Router ignored
- [ ] 2. Recurring friction
- [ ] 3. AGENTS.md size
- [ ] 4. `.agents/` contradictions
- [ ] 5. Token-heavy loads
- [ ] 6. Stale capsules
- [ ] 7. New agent gap
- [ ] 8. Patterns INDEX drift
- [ ] 9. Wrong rails on PRs
- [ ] 10. Validator noise

## Active symptoms
<list>

## One action retained
> <imperative>

Lands in: <file>
```
