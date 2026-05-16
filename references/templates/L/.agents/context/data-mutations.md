# Data mutations — capsule

Doctrine for any code path that **writes** to the system of record (database, persisted state, external API with side effects). Load this when the task touches mutation logic, optimistic UI, rollback, or write-path consistency.

> Example capsule — replace its content with your project's actual mutation doctrine. The structure (Doctrine / Patterns / Anti-patterns / Pivot files / Validation) is what matters.

## Doctrine

1. **The server is the source of truth.** Client state is a view over it. Any optimistic update must have an explicit rollback path.
2. **One concurrent in-flight per logical key.** Two writes to the same logical entity (same user, same task, same draft) must not race. Use a key-based in-flight guard, a queue, or `cancelQueries` (TanStack Query) — pick one and document it.
3. **Never silently swallow a mutation error.** Errors surface to the user (toast, banner, inline state). A failed mutation that "looks like it worked" is the worst kind of bug.
4. **Idempotency where possible.** Operations that may be retried (network flakiness, optimistic resync) should be safe to apply twice. Use deterministic IDs from the client when feasible.

## Patterns

### Optimistic update with rollback

```
1. Capture previous state (snapshot)
2. Apply optimistic mutation to local cache
3. Fire the network call
4. On success: reconcile with server response
5. On failure: restore snapshot, surface the error
```

### TanStack Query optimistic mutation (if applicable)

```
await queryClient.cancelQueries({ queryKey })   // ALWAYS first
const previous = queryClient.getQueryData(queryKey)
queryClient.setQueryData(queryKey, optimisticValue)
try {
  await mutate(input)
} catch (err) {
  queryClient.setQueryData(queryKey, previous)
  surfaceError(err)
}
```

### Server-driven write (when available)

If the project has a worker / edge function / RPC for writes, prefer routing through it. The client orchestrates the optimistic UI; the worker owns the canonical write.

## Anti-patterns to refuse

- Optimistic UI without rollback. ("It'll usually succeed" is not a contract.)
- Two mutation calls firing on the same logical key without coordination.
- Manual `setQueryData` without prior `cancelQueries` (polling-in-flight will overwrite you).
- Catching a mutation error and continuing as if nothing happened.
- "Just a single insert" performed directly against the DB from the client when the project has a server write-path.

## Pivot files in the codebase

| File | Role |
|---|---|
| `<src/hooks/use*Mutation.ts>` | mutation handlers |
| `<src/services/api.ts>` or RPC client | network layer |
| `<src/queries/*>` | query key definitions / cache layout |

## Validation when editing this zone

- `<typecheck>` after every change.
- Targeted unit tests on the mutation handler (happy path + rollback path).
- A smoke or integration test if the mutation crosses the network boundary.

## When to update this capsule

- A new pattern (or anti-pattern) emerged from a `/learn` entry → diffuse here.
- A pivot file moves or splits → update the table.
- The doctrine itself shifts (e.g. you adopt server write-path migration) → consider promotion to a dedicated pattern at L.

Hard cap: 150 lines. If this capsule grows past 150, refactor (split by sub-domain) — it stopped being a focused capsule.
