# <Project Name> — STATUS APP (Source of Truth)

Date: <YYYY-MM-DD>
Branch of reference: `main`
Last production deploy: `<sha or tag>` (<YYYY-MM-DD>) — <one-line note: what was shipped, validation outcome>
Recent scope: <one-line description of the current cycle / focus>
Next milestone: <one-line description>

---

## 1. Snapshot

- Runtime: <one line — e.g. "S2 active: REST/RPC + TanStack Query, Realtime under feature flag">
- Critical zones state: <one line per zone, current status>
- Active feature flags: <list, with default values>
- Open architectural questions: <if any, point to ADR draft or open ticket>

## 2. Progress (axes → state → evidence)

| Axis | State | Evidence |
|---|---|---|
| <Functional area 1> | DONE / IN_PROGRESS / BLOCKED | <files, PRs, or commands> |
| <Functional area 2> | DONE / IN_PROGRESS / BLOCKED | <files, PRs, or commands> |
| <Functional area 3> | DONE / IN_PROGRESS / BLOCKED | <files, PRs, or commands> |

States:
- `DONE` — landed in `main` and validated in the target environment
- `IN_PROGRESS` — under active work
- `BLOCKED` — explicit blocker noted in the evidence column

## 3. Current release checklist

Use this section only when a release / candidate is in flight. Strike out (or remove) when not applicable.

- [ ] Scope merged on `main`
- [ ] `<typecheck>` + `<test>` + `<smoke>` green
- [ ] PR rail review done
- [ ] Release doc generated (if applicable)
- [ ] Preprod / staging validated
- [ ] Production deploy executed
- [ ] `/retro` invoked within 24h after deploy

## 4. Recent decisions

Short ledger of decisions taken since the last release. Newest on top. One line per decision, link the ADR or the discussion if any.

- <YYYY-MM-DD> — <decision in one sentence> — see <ADR-XXX | PR #N | discussion>
- <YYYY-MM-DD> — <decision in one sentence>

## 5. Known debt / signals to watch

- <one-line item — e.g. "CI minutes consumption approaching free-tier limit">
- <one-line item — e.g. "Auth path X relies on legacy mechanism Y until ADR-Z is closed">

## 6. Active references

- `WORKFLOW.md` (process, branches, CI)
- `AGENTS.md` (universal agent contract)
- `CLAUDE.md` (Claude adapter, if applicable)
- `.agents/ROUTER.md` (task routing)
- <link other documents that matter right now — ADRs, runbooks, roadmaps>
