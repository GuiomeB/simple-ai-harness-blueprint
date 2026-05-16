# Router — task family → context

Load the **minimum** context useful for the task at hand. Doesn't replace `AGENTS.md` (always implicit, already loaded). Routes to the right capsule, workflow, or skill.

## Loading order

1. `AGENTS.md` (implicit) — invariants, commands, validation matrix.
2. Identify the **task family** in the table below.
3. Load the **pivot capsule** + 0..N complements listed.
4. Activate the skill or workflow indicated if the scope matches.
5. If the task reveals a recurring procedure, update or add a capsule.

> The minimum validation per zone lives in `AGENTS.md §Minimal validation matrix` — not duplicated here.

## Routing table

> The first row below is a **worked example** wired to the `data-mutations.md` capsule shipped with this template. Replace or delete it if mutations aren't a critical domain in your project, and add rows for your own domains.

| Task family | Pivot capsule | Complements | Skill / workflow |
|---|---|---|---|
| Data mutations, optimistic UI, rollback, write-path consistency | `context/data-mutations.md` | mutation hook files, query-key definitions | `/tdd-loop` if behaviour change |
| <Domain 2 — e.g. auth, sessions, identity> | `context/<domain-2>.md` | <list of files / docs> | <skill name or workflow> |
| <UI / design-system / component conventions> | `context/<ui-doctrine>.md` (if you have one) | <component files, ViewModel files> | `<skill name>` if any |
| <PR preparation / merge / risk rail classification> | (no capsule needed at M) | `WORKFLOW.md`, `.github/pull_request_template.md` | none required |
| <Release / deploy / candidate> | (no capsule needed at M) | `STATUS_APP.md`, `WORKFLOW.md §release` | `/retro` after a release |
| <Retro, friction, refactor learning> | (no capsule needed) | `STATUS_APP.md` if scope is project-wide | `/retro` (release) or `/learn <scope>` |
| <Tests, fixtures, smoke scripts> | (no capsule needed at M) | the test file of the domain concerned, `.agents/workflows/tdd-loop.md` | none |
| <Updating the agent system itself (this file, capsules, `AGENTS.md`)> | this file | `WORKFLOW.md` | none |

Add one row per critical domain that has a capsule. Don't pre-create rows for capsules that don't exist yet.

## Choosing between adjacent families

- **Mutation client vs server write-path** → if the write is launched from the client and propagated by an API/RPC call, that's *client mutation*. If the write is owned by a server / worker / edge function, that's *server write-path*.
- **UI domain vs large refactor** → visual scope, component, tokens: *UI domain*. Logic debt, file > 200 lines, deep nesting: *large refactor* (`/code-refactor` at L if available).
- **Retro vs Learn** → after a release of a cycle (GO or NO-GO): `/retro`. Incident, no-go candidate, recurring friction, marker refactor: `/learn`.

## Loading rules

- Don't load `STATUS_APP.md` by default for small local tasks. Reserve it for release, runtime, auth, or roadmap topics.
- For a small UI task, the project's UI doctrine (if any capsule exists) prevails over generic frontend habits.
- For a critical-zone change, load the pattern (at L) before editing.
- Never load more than **3 capsules simultaneously** for a single task. If it feels like more, the task is over-scoped — split it.
