---
name: simple-ai-harness-blueprint
description: Install, audit, or extend an AI-collaboration blueprint on a code repository — the AGENTS.md / CLAUDE.md / .agents/ structure that lets AI agents (Cursor, Claude Code, Codex Desktop/CLI, Windsurf) collaborate without drift. Three additive sizes (S/M/L). Trigger when bootstrapping a new repo's AI scaffold, promoting an existing harness to the next size, or auditing one for sprawl.
---

# Simple AI Harness Blueprint

A scaffold for repos where AI agents and humans collaborate. Three sizes (S/M/L), strictly additive — filenames never change between levels.

## When NOT to use

Skip for product code, PR reviews, IDE configuration, or generic project scaffolding.

## Doctrine — the 4 Karpathy rules

Every `AGENTS.md` generated opens with these. They override convenience and other rules in conflict.

1. **Don't assume. Don't hide confusion. Surface trade-offs.** Ambiguity → ask before coding.
2. **Minimal code that solves the problem. Nothing speculative.** No preventive abstractions.
3. **Touch only what's necessary. Clean up only your own traces.** Diff = scope of the ticket.
4. **Define success criteria. Loop until verified.** State the verifiable criterion before acting.

## Pick the size

Depths of harness, not codebase sizes. Match signals:

| Signal | S | M | L |
|---|---|---|---|
| AI agents in regular use | 1+ | 1–3 | 2+ rotating |
| Human contributors | Solo | Solo or 2–3 | 2+ |
| Deployment criticality | Local / hobby / early stage | Public / users | Production / regulated |
| Project age with active agent edits | < 3 months | 3–12 months | 12+ months |
| Friction "the agent forgot rule X" | Rare or absent | Recurring | Painful or routine |
| Critical zones to protect | 0–1 | 2–5 | 5+ |
| Existing `AGENTS.md` state | None, or close to the ~100–150 line S baseline | Growing past 150 lines | Past 250 lines, hard to navigate |

Two or more signals at a level → adopt that level. Never jump straight to L on a fresh repo.

**Note on the `AGENTS.md` signal:** a freshly-generated S `AGENTS.md` is itself ~100–150 lines (4 Karpathy rules + critical zones + commands + rail rule + load order). When reading this signal, look at *project-specific accretion on top of the baseline*, not the raw line count.

## Tree per size

Every level is strictly additive: filenames never change between sizes, you only *add*.

### S — minimum with all 3 mechanisms present

```
your-repo/
├── README.md
├── AGENTS.md                            M1 (load order) + 4 Karpathy + critical zones + commands + M3 rail rule
├── CLAUDE.md                            optional adapter — include only if Claude is a used agent
├── WORKFLOW.md                          process + when to invoke /learn (refers to AGENTS.md for rail discipline)
└── .agents/
    └── workflows/
        └── learning-loop.md             M2 — /learn per-event capture
```

### M (additive over S) — routing + status + formalized PR flow

```
+ STATUS_APP.md                           living log: current stage, recent decisions, known debt
+ .agents/
│   ├── ROUTER.md                         task family → context capsule matrix
│   ├── context/
│   │   └── <critical-domain>.md          1–3 capsules per project; 80–150 lines each
│   └── workflows/
│       ├── retro.md                      post-release retrospective workflow
│       └── tdd-loop.md                   optional but typical at M
+ docs/retro/                             output of /retro
+ .github/
    └── pull_request_template.md          M3 formalized: risk rail declaration in PR body
```

### L (additive over M) — full system, machine-enforced

```
+ .agents/
│   ├── patterns/
│   │   ├── INDEX.md                      registry: pattern ↔ pivot files in the codebase
│   │   └── <action-pattern>.md           short copyable procedures (≤ 120 lines)
│   ├── rules/
│   │   └── <tech-convention>.md          narrow technical rules (test signatures, smoke scripts)
│   └── skills/
│       └── <project-skill>/SKILL.md      project-specific skills / Claude skills where applicable
+ docs/
│   ├── adr/                              Architecture Decision Records
│   └── learn/                            per-event /learn output (auto-created on first run)
+ scripts/
│   ├── validate_agent_context.*          meta-CI: the harness validates its own coherence
│   └── check_pr_rail_consistency.*       rail-guard: fails `green` PRs that touch CODEOWNERS paths
+ .github/
│   ├── CODEOWNERS                        source of truth for "critical paths"
│   └── workflows/
│       ├── agent-context.yml             non-blocking signal on .agents/** changes
│       └── pr-rail-guard.yml             blocking gate on PR risk rail consistency
+ _local/CI_RULEBOOK.md                   optional, gitignored: rationale of CI/agent choices
```

## File size budgets

| File | Soft target | Hard ceiling |
|---|---|---|
| `AGENTS.md` | 100–150 | 300 |
| `CLAUDE.md` | 40–60 | 100 |
| `WORKFLOW.md` | 150–200 | 300 |
| `STATUS_APP.md` | unbounded (log) | n/a |
| `.agents/ROUTER.md` | 40–60 | 100 |
| `.agents/context/*.md` | 80–150 | 200 |
| `.agents/patterns/*.md` | 40–120 | 200 |
| `.agents/workflows/*.md` | 80–200 | 300 |
| `.agents/skills/*/SKILL.md` | ≤ 200 | 500 |

**Session-init budget:** keep total auto-loaded context ≤ **6 500 lines** across all files an agent reads before its first action. Trade per-doc ceilings against this total — a leaner `ROUTER.md` leaves room for a fatter `WORKFLOW.md`, and vice versa.

## The 3 mechanisms — templates only

### M1. Init: ordered context load (lives in `CLAUDE.md` or the agent's adapter file)

Two progressive forms — the order grows one hop once the ROUTER exists.

**At S** (no ROUTER yet):

```markdown
Before generating code for any new request, load context in this order:
1. AGENTS.md (project contract — implicit, never skip)
2. files directly touched by the request
3. additional documentation only if the task obviously requires it
Never load large documents "just in case".
```

**At M and L** (ROUTER present):

```markdown
Before generating code for any new request, load context in this order:
1. AGENTS.md (project contract — implicit, never skip)
2. .agents/ROUTER.md (identify task family, pick minimum context)
3. the capsule / pattern the router points to (if any)
4. files directly touched by the request
5. additional documentation only if the router points to it
Never load large documents "just in case".
```

Always restate the active form in `AGENTS.md §Role` so the rule survives careless edits to the adapter.

### M2. Learning: per-event capture (lives in `.agents/workflows/learning-loop.md`)

```markdown
# /learn workflow
Invocation: /learn <family> <slug>
Families: release | candidate | incident | friction | refactor

Output: docs/learn/LEARN_<family>_<slug>_<YYYY-MM-DD>.md (≤ 40 lines):
- What helped (2–4 bullets)
- What slowed us down (2–4 bullets)
- ONE action retained (imperative, < 20 words)
- "Lands in: <target artefact>"
- Diffusion: files actually changed

Then update the target artefact and run `validate:agent-context`.
Hard constraint: ONE action per /learn.
```

### M3. Risk rail enforcement (3 progressive forms)

The rail concept lives at every level — only the *enforcement strength* grows.

**At S — agent self-declaration in `AGENTS.md`** (no PR flow required):

```markdown
## Risk rail (declare after every task)

After completing any task or before pushing/committing changes, declare a rail
in your message:

- Rail: green | amber | red

green = small/local; no critical zone touched; safe to merge fast
amber = behavioural or transverse; the user should scan the diff
red   = critical path or production risk; the user must review

The rail is informational at this stage (no CI enforcement). Its value is
forcing the agent to self-assess sensitivity, and the user to see it.
```

**At M — formalized PR template** at `.github/pull_request_template.md`:

```markdown
## Risk rail
- Rail: green | amber | red

green = small/local; no CODEOWNERS path; no runtime/auth/release touch
amber = behavioural or transverse; short human review or owner approval
red   = critical path or production risk; full review mandatory

Touching a .github/CODEOWNERS path → minimum amber.
P1/P2 finding during review → automatic red until resolved.
```

**At L — machine enforcement**:

- CI job `pr-rail-guard`: fail PRs declared `green` that touch any path listed in `.github/CODEOWNERS`
- Meta-validator `scripts/validate_agent_context.*`: check every `npm run X` cited in `AGENTS.md` exists in `package.json`, every internal link in `.agents/**` resolves, and `patterns/INDEX.md` covers every pattern file

## Codex Desktop compatibility

This repository is both a Claude skill and a Codex Desktop skill. Codex reads the same `SKILL.md` frontmatter/body; `agents/openai.yaml` only adds optional UI metadata. Do not fork the instructions by agent. Keep `AGENTS.md` canonical and use thin adapters (`CLAUDE.md`, `GEMINI.md`, etc.) only when a tool requires a specific entry file.

## Workflow for invoking this skill

1. **Inventory.** List existing blueprint files in the target repo.
2. **Infer and propose — don't interrogate.**
   - **Size:** match the matrix above to repo signals — `AGENTS.md` line count, presence of `.agents/`, multi-agent traces, `.github/`, codebase age.
   - **Agent adapters:** scan for markers — `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `GEMINI.md`, etc. Include each adapter only if its marker is found, the user names that agent explicitly, or the user explicitly says "Claude" / "Cursor" / etc. is in use. `AGENTS.md` is always included.
   - **PR workflow:** detect `.github/`, `.gitlab/`, branch-protection rulesets. Add `.github/pull_request_template.md` only at M+ *and* if a GitHub-compatible PR flow is detected.
   - **Propose in one sentence with reasoning**, e.g. "Based on no existing `AGENTS.md`, a `.cursorrules` file, and a `.github/` folder, I'd target **M**, with `CLAUDE.md` (you mentioned Claude) and `.github/pull_request_template.md`. Confirm or adjust?"
   - Ask explicit questions **only** when inference is genuinely ambiguous (multiple plausible sizes, conflicting agent markers, or the user contradicts the inference).
   - If existing artefacts exceed the requested level, warn about downgrade risk before removing anything.
3. **Generate the delta.** For each missing file, propose the matching template from `references/templates/<size>/`. Confirm before writing. Never overwrite silently. **Follow placeholder discipline (see below): do not invent commands, files, or critical zones the target repo doesn't have.**
   - The M templates include one **worked example** (a `data-mutations.md` capsule and a matching row in `ROUTER.md`) to model after. Replace or delete the example if mutations aren't a critical domain in the target project, and route the user's own capsules instead.
4. **Validate.** Print the created tree, run any present `validate:agent-context`, ask the user to skim `AGENTS.md` first.
5. **Plant the next promotion criterion AND report remaining placeholders.** Add a one-line "promote to next size when X" at the bottom of `AGENTS.md`. Then list every `<placeholder>` left in the generated files (commands, critical zones, project description, etc.) so the user knows exactly what to fill in before the harness becomes operational. An unfilled placeholder is the correct state — a *filled* one with invented content is a lie.

## Adopting on an existing repo

If the target repo already has its own agent doctrine, **never overwrite**:

- Don't replace an existing `AGENTS.md`. Propose an *additive merge*: keep the project's accreted rules, insert universal sections (4 Karpathy rules, load order, rail discipline) only where they're missing.
- Don't create a parallel `.agents/` if the repo uses a different layout (`.cursor/rules/`, `.windsurf/`, custom paths). Adapt: place equivalent content there and note the divergence at the top of `AGENTS.md`.
- Look for what's *missing*, not for what doesn't match this template. The blueprint's value on a mature repo is usually three things: **navigation** (ROUTER at M), **drift check** (`validate_agent_context.*` at L), **per-event learning loop** (`/learn`). Add only those.

A mature repo with a working memory should be enhanced, not rescaffolded.

## Placeholder discipline

Templates ship with `<...>` placeholders (e.g. `<run dev>`, `<typecheck>`, `<critical-zone>`, `<path/to/file.ts>`). They are intentional — they mark what the project hasn't decided or doesn't have yet.

**Hard rule:** never replace a placeholder with an inferred value. Replace only when one of these is true:

- The actual file or tool already exists in the target repo, and you have read or listed it.
- The user has explicitly named the value (e.g. "I use `ruff` and `pytest`" → fill `<lint>` and `<test>`).
- The user explicitly asked you to scaffold product code too (rare; outside this skill's default boundary).

If you don't know, **leave the placeholder**. Empty placeholders tell whoever opens the file what's not yet decided. A filled placeholder with invented content is a lie that compounds over time and rots the harness quickly.

A user prompt mentioning a language or framework ("Python CLI", "Next.js side-project", "React + Node API") is a *hint about direction*, not a *guarantee that tooling exists*. The repo is the source of truth; the user's words are clues for what to ask about, not licenses to assume.

When the bootstrap is done, the report from step 5 of the workflow must enumerate every remaining `<placeholder>` so the user can fill them deliberately.

## Health metrics

| Symptom | Cause | First fix |
|---|---|---|
| Agents ignore the router | Init rule buried | Restate at top of `AGENTS.md §Role` |
| Same friction reported 3+ times | `/learn` never ran | Run one `/learn friction` retroactively |
| `AGENTS.md` > 300 lines | Domain doctrine in constitution | Extract to `.agents/context/<domain>.md` |
| `.agents/` files contradict | No validator | Add `validate_agent_context.*`; schedule a `/retro` |
| Token-heavy loads for trivial tasks | ROUTER too permissive | Tighten rules; mark files "do not load by default" |
| Capsule untouched 3+ months | Doctrine stable or zone dead | Inline into `AGENTS.md` or delete with an ADR |
| New agent ignores rules | Reads a different config file | Symlink or copy `AGENTS.md` to its expected name |

Two or more symptoms simultaneously → schedule rework.

## References

- `references/templates/S/`, `M/`, `L/` — copyable file templates per level
- `references/health-metrics.md` — extended diagnostics

## Boundaries

Operates only on the documentation surface agents read. Does not touch product code, run tests, configure IDEs, or decide architecture.
