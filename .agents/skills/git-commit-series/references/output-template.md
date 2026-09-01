# CommitPlan handoff template

Render the plan in this order so a reviewer or execution agent can scan the
series without reconstructing hidden state. Field meanings come from
plan-schema.md.

~~~md
# Commit series handoff

Mode: plan | execute | history-edit
Schema version: 1
Base: <ref> (<sha>)
Branch: <branch or detached HEAD>
Baseline: <index/worktree summary>
Ordering basis: <dependency evidence and deterministic tie-break>

## Protected changes
- <Hxxx> <path> — <reason>
- None

## Undecided changes
- <Hxxx> <path> — <decision ID and reason>
- None

## Residual changes
- <Hxxx> <path> — <why deferred>
- None

## Dependency order
1. C1
2. C2 (after C1)
3. C3 (after C1, C2)

## Commits

### C1 — <status>

Operation
<history operation, or “none” for a worktree change>

Subject
<subject>

Body
<body, or “none” when the repository accepts a subject-only message>

Trailers
- <trailer>
- None

Intent
<one sentence answering why this commit exists>

Hunk ownership
- H001 — <basis> <path>: <anchor> — <summary> [<classification>; fingerprint: <value or none>]
- H002 — <basis> <path>: <anchor> — <summary> [<classification>; fingerprint: <value or none>]

Files
- <path>

Depends on
- None

Validation
- G1 — <command> — <purpose>
  - Expected: <expected>
  - Result: pending | passed | failed | not-run
  - Evidence/reason: <output or explanation>

Risk and rollback
- Risk: <risk>
- Rollback: <rollback effect>

Expected state
<state after this item is applied>

Notes
<notes, or “none”>

### C2 — <status>
<repeat the same fields>

## Excluded changes
- <Hxxx> <path> — <reason>
- None

## Open decisions
- <Dxxx> <question>; affected: <hunk IDs>; recommendation: <option>
- None

## Handoff
<What the next agent may execute, the authorization still required, and any
baseline-change condition.>
~~~

## Rendering rules

- Use the exact stable IDs from the plan object.
- Show hunk ownership before the file summary; files are only a convenience
  view.
- Preserve repository-native subject, body, and trailer conventions. Render
  the complete message without imposing a language or length rule.
- Show validation states literally. A pending or not-run gate remains visible.
- Put every protected, excluded, residual, and unresolved item in a named
  section, including an explicit None when empty.
- In plan mode, state that no Git mutation occurred. In execute or history-edit
  mode, add each actual hash and deviation next to its corresponding item.
- Keep recommendations separate from decisions. An unresolved boundary is
  represented as an open decision rather than silently adopting the
  recommendation.
