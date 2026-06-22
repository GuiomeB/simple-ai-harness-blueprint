# Explanations — why this blueprint exists, what was learned along the way

> This file is **not** part of the skill. The skill itself (`SKILL.md`) never loads it. It's pedagogical material for someone who clones this repo on GitHub and wants to understand the *why* behind each choice before adopting any of it.

If you only want to install and use the blueprint, `README.md` is enough. Come back here if you find yourself disagreeing with a rule, wondering why we ship 3 patterns instead of 30, or asking "did anyone actually use this on real projects?"

---

## What problem this exists to solve

I've been building software with AI coding agents (Claude Code, Cursor, Codex CLI, Antigravity, Windsurf) for long enough to recognize three recurring failures on every real codebase I've tried it on:

**1. Amnesia.** An agent reads `CLAUDE.md` (or `AGENTS.md`, or `.cursorrules`) at the start of a session, then forgets half of it by message 20. By message 40 it's coding as if no doctrine exists. The fix isn't a longer config file — it's a *load order* the agent re-applies every request, plus a *router* that loads only what's relevant.

**2. Sprawl.** Every agent wants its own config file. After three months you have `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `GEMINI.md`, and the rules diverge silently. Each new contributor (human or agent) is a chance to introduce a fourth file. The fix is one universal contract (`AGENTS.md`) and thin agent-specific adapters that only restate the load order.

**3. Drift.** Rules accreted six months ago no longer match the code. The agent reads stale doctrine and writes obsolete code, confidently. The fix is a meta-validator that checks the harness against the codebase, plus a learning loop that turns each friction into one specific edit to the right artefact.

This blueprint is what I ended up with after running into those three problems on multiple projects — including one I worked on full-time for several months as the laboratory for this approach.

---

## The five Karpathy rules + M0 — why this shape

The rules at the top of every `AGENTS.md` this blueprint generates aren't original. They've been circulating in the AI-coding community since Andrej Karpathy popularized them (well written up by [Yanli Liu](https://yanliu.medium.com/the-4-rules-of-coding-with-llms-from-karpathy-d3a1c9bd6b66) and others). This blueprint ships a **revised five-rule form** plus a separated verification mechanism (**M0**) — the lineage is Karpathy's, the revision is this project's.

What changed from the original four, and why:

- **Posture and mechanism were split.** The original rule 4 ("define success criteria, loop until verified") is not really *posture* — it's the verification *mechanism* every task runs. Burying it as one bullet among behavioural rules made it the most-skipped one. It's now **M0**, a first-class mechanism stated right after the five rules, with an operational form (trigger · stop criterion · validation · budget · stop/no-progress). The validation matrix, the DoD, `/tdd-loop`, and the L+ `/loop` all inherit from it.
- **Rule 1 now carries an autonomy clause.** "Ask, don't assume" is unchanged for interactive work, but explicitly scoped: *only* in an activated autonomous mode (L+) does the agent pick the most reasonable interpretation and record the assumption instead of blocking. This keeps the default conservative while making unattended loops possible without contradicting the rule.
- **Rule 3 now says what to do with smells.** "Don't touch unrelated code" used to imply silence. The revision adds the missing half: surface bad code or design smells as a *separate* issue. Scope discipline shouldn't cost you the signal.
- **Two genuinely new posture rules.** Rule 4 (flag uncertainty explicitly, prefer a small low-risk experiment over false confidence) and rule 5 (suggest better, lasting-impact approaches) encode collaboration behaviours the original four didn't.

What makes the set right *for this blueprint*:

- **They're behavioural, not technical.** They translate across stacks. A team using TypeScript + React and a team using Python + FastAPI both benefit from the same five.
- **They're short enough to actually be re-read every session.** A 50-rule "agent ethics document" gets skimmed. Five rules with one sentence each get internalized.

The order matters: rule 1 (ask, don't assume) is the most often violated; M0 (verification) is the most often skipped — which is exactly why it was promoted out of the list into its own mechanism.

---

## S / M / L — why depth, not size

Most "AI-ready" templates I've seen come in one size: the maximalist one. They ship 12 files on day 1, half of which the project will never touch. New users adopt them, get overwhelmed, delete half, and end up worse off than with no template at all.

The S/M/L approach trades comprehensiveness for *fit*:

- **S** — minimum that still gives value. Four to five files. All three mechanisms (Init, Learning, PR-time discipline) are present, just in their simplest form. A solo dev on a hobby project still gets the learning loop, the load order, the rail discipline. They just don't get a router, capsules, or patterns yet — because they don't have enough doctrine *to route to*.
- **M** — the sweet spot. The router enters the system. Domain-specific doctrine moves out of `AGENTS.md` and into capsules. The PR template formalizes the rail. The retro workflow joins the learning loop. About 80% of the value, for the projects that have outgrown S but don't yet need machine enforcement.
- **L** — full system. Patterns, rules, project-specific skills, ADRs, the meta-validator, and the machine-enforced rail-guard. Right for a production codebase with multiple agents and real release discipline.

The key property: **filenames never change between sizes**. Promoting from S to M is purely additive. You add files, you don't rename them. So a project can grow into the blueprint at its own pace, without ever having to refactor what's already in place.

A note on signals: S/M/L is *not* a function of codebase size. A 2 kLoC side-project with three different AI agents in regular use needs M. A 50 kLoC monolith with one occasional contributor can live at S. The signal that matters is *recurring agent confusion*, not lines of code.

---

## The three mechanisms — what was tried, what stuck

The blueprint codifies three behavioural mechanisms. Each went through experimentation before landing on its current form.

### Init — ordered context load

**What this is:** a strict load order the agent re-applies on every new request: `AGENTS.md` → `ROUTER.md` (M+) → capsule → files touched → additional docs. Lives in the agent's adapter file (`CLAUDE.md`, etc.) and is restated inside `AGENTS.md` so it survives careless adapter edits.

**What didn't work:** trying to enforce it via the IDE. Most IDEs don't expose session-init hooks. Even when they do, the agent often re-interprets them in surprising ways. The most reliable mechanism remains *prose* — the agent reads the load order and (mostly) follows it.

**Why the rule survives in prose:** because we re-state it in two places (the adapter and `AGENTS.md`), so it survives even if one is edited carelessly.

### Learning — per-event capture, not rolling log

**What this is:** `/learn <family> <slug>` and `/retro <date>` workflows. Each invocation produces one short audit-trail file under `docs/learn/` or `docs/retro/`, **and** diffuses exactly one action to the most actionable artefact (a capsule, a rule, a pattern, or `AGENTS.md` itself).

**What didn't work:** the obvious first attempt was a single growing `friction-log.md`. People stopped reading it after week three. The log became a graveyard, not a tool. The deeper problem: a rolling log accretes without forcing a decision. You can write a friction in 30 seconds and feel productive without ever fixing anything.

**Why per-event works:** each `/learn` is a *transaction*. You can't close it without (a) deciding the one action, (b) editing the right artefact, (c) writing the trace file. The hard constraint "one action retained" is the friction that makes the system improve.

This is the mechanism I'd save first if I had to keep only one from this blueprint.

### PR-time enforcement — three progressive forms

**What this is:** the risk-rail discipline (`green` / `amber` / `red`). At S it lives as a self-declaration rule in `AGENTS.md`. At M a `pull_request_template.md` formalizes it. At L a CI gate (`pr-rail-guard`) actually fails mismatched declarations against `.github/CODEOWNERS`.

**What didn't work:** trying to ship CI enforcement on day 1. Most projects don't have `CODEOWNERS` discipline yet — and machine-enforcing a rail without a clear source of truth for "what counts as critical" produces noise. The progressive form lets the project earn its way to enforcement.

**The non-obvious value at S:** even without CI, the *act of declaring* a rail in your message forces the agent to self-assess sensitivity. Half the value of the rail isn't catching mistakes — it's making sensitivity visible to the user at a glance.

---

## What was tried and abandoned

For honesty, here are ideas that seemed promising and turned out to underperform:

- **A single rolling `friction-log.md`.** Replaced by per-event `docs/learn/LEARN_*.md` files. The rolling log invited entropy.
- **A pattern that overlapped a capsule and a workflow.** I once shipped a "capture learning loop" as a pattern, a capsule, *and* a workflow simultaneously. Three angles on the same thing. The user (me) couldn't remember which to invoke. Consolidated: the workflow is invocable, the capsule carries doctrine, no pattern needed.
- **Pre-creating all `.agents/context/` capsules on day 1.** Most stayed empty and rotted. Now: capsules are added only when the *third* friction in the same domain occurs.
- **Bigger is better for the universal contract.** Earlier versions had a 250-line `AGENTS.md` packed with examples. Agents skipped 80% of it. The current target is 100–150 lines.
- **A separate `.cursorrules` / `CLAUDE.md` / `GEMINI.md` file per agent.** Rules drifted instantly. Now: `AGENTS.md` is universal, agent-specific files are thin adapters.

---

## Comparison with adjacent approaches

A few things this blueprint is and isn't:

- **vs. `mex` and similar scaffold tools.** `mex` (and its cousins) generate a generic scaffold for any project. If your repo has nothing yet, that's useful. If your repo already has a working memory (a real `AGENTS.md`, retros, ADRs), installing a generic scaffold *replaces* what works. This blueprint takes the opposite approach: on an existing repo, propose an *additive merge*, never an overwrite. See `SKILL.md §Adopting on an existing repo`.
- **vs. plain `CLAUDE.md` / `AGENTS.md`.** A flat config file works for tiny projects. It rots fast at scale, because there's no router and no learning loop. The blueprint adds the missing two layers without forcing you to start at L.
- **vs. language-specific scaffolds (cookiecutter, create-react-app, …).** Those generate code structure. This blueprint generates *collaboration structure*. They're complementary, not competing.

---

## Adopting this on an existing repo

If your repo already has agent doctrine, **don't overwrite anything**. Three principles:

1. **Keep what works.** A `CLAUDE.md` you've been refining for six months has captured real knowledge. The blueprint's universal sections (5 Karpathy rules + M0, load order, rail discipline) go *next to* yours, not *over* yours.
2. **Add navigation, not redundancy.** The blueprint's biggest value on a mature repo is usually three things: a router (`.agents/ROUTER.md`), a per-event learning loop (`/learn`), and a drift check (the meta-validator at L). Add those three and almost everything else is gravy.
3. **Adapt the layout.** If you use `.cursor/rules/` or `.windsurf/` instead of `.agents/`, the blueprint's structure is documentation, not law. Place the equivalent content where your existing layout puts it, and note the divergence at the top of `AGENTS.md`.

A mature repo with a working memory should be *enhanced*. Re-scaffolding rarely pays off.

---

## What's missing, what's next

This is v1. Known gaps:

- **No machine-readable evaluation harness.** I'd like to ship a small test suite that, given a target repo and an expected level, asserts the blueprint has been applied correctly. Not yet here.
- **The IDE-side init hook is still prose-only.** When IDEs expose session-start hooks, the load order should wire there.
- **The validator is intentionally minimal.** It catches the obvious failures (broken links, orphan patterns, missing capsules), not deep semantic drift. A deeper validator is possible but starts to compete with general code review.
- **No per-language guidance.** Patterns are generic. Whether to ship a `templates/python/` or `templates/typescript/` subfolder with language-specific examples is an open question.

If you adopt the blueprint and find something missing — open an issue. The whole point is that the system *learns*; this repo should too.

---

## A note on attribution

The Karpathy rules are not mine — the lineage is his; the revised five-rule form and the M0 split are this project's adaptation. The S/M/L framing is mine, but obviously inspired by every "starter / advanced / expert" tiering you've seen. The per-event learning loop emerged from running a real project where a rolling log demonstrably didn't work; I don't claim it's a novel idea, but I do claim the specific shape (one action retained, lands in an executable artefact, audit trail in a per-event file) is what made it stick on my projects.

If a pattern in here helps you, take it. If a pattern doesn't help you, drop it. The blueprint is opinionated, not dogmatic.
