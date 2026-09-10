# Implementation Record contract

An Implementation Record preserves what implementation discovered after or during design. It is
historical and implementation-specific. An ADR remains the sole authority for a durable
architecture choice; a test or Sensor remains the authority for executable behavior; a public API
comment or canonical API reference remains the authority for consumer-facing contract text.

## Location and lifecycle

Follow the repository's existing documentation convention. If none exists, use
`docs/implementation/records/<slug>.md`. Create a record when findings span multiple placements,
one material compatibility, failure, security, migration, or drift finding needs durable context
beyond code and a sensor, or the user or repository requires an implementation handoff. A local
finding fully carried by code and its sensor may close with `record not warranted`.

Update a `draft` record at implementation checkpoints. Once it is `complete`, preserve it as the
historical account of that increment. Later implementation work gets a new linked record; use
`superseded` only when the newer record intentionally replaces the older record's conclusions.

Use these record statuses:

- `draft` - capture is in progress or verification is incomplete;
- `complete` - every finding has a placement and the stated checks have been run or marked;
- `superseded` - a later record owns the implementation knowledge; link it;
- `blocked` - a required capture or verification step cannot proceed; name the owner and next check.

Use `confirmed`, `inferred`, `unknown`, `not-run`, and `blocked` for row-level evidence and
sensors. Do not use a successful test to upgrade an architectural inference that the test does
not measure.

## Required shape

```markdown
# Implementation Record: <slug>

Date: YYYY-MM-DD
Owner: <person or team>
Status: draft
Baseline: `<branch>@<sha>`
Authorization: <scope>

## Purpose
<Why this record exists and what it preserves.>

## Scope
<Implemented and explicitly deferred surfaces.>

## Inputs
<Links to Briefs, ADRs, Probes, issues, or requirements used by the implementation.>

## Public API coverage
Include this section only when the public API documentation branch fires.

| Surface | Kind | Scope | Documentation | Coverage check | State |
| --- | --- | --- | --- | --- | --- |
| `PackageName` | exported module | intended public symbols | source declarations | native API-doc or declaration check | confirmed |

## Implementation sequence
<Only steps whose order explains a decision; otherwise None - reason.>

## Rationale ledger
| ID | Finding/observation | Evidence | Impact if changed | Placement | State |
| --- | --- | --- | --- | --- | --- |
| R1 | ... | ... | ... | ... | confirmed |

## Comment and sensor map
| ID | Source location | Role | Link or check | State |
| --- | --- | --- | --- | --- |
| R1 | `src/module.ts:42` | source rationale | `tests/module.test.ts` | confirmed |

## Verification
| Check | Command | Environment | Result | State |
| --- | --- | --- | --- | --- |
| focused tests | `project test command` | runtime/toolchain versions | result and limits | confirmed |

## Drift and decisions
<Differences from accepted design, ADR updates, or None - reason.>

## Remaining boundaries
<Known limitations, unrun checks, owners, and next checks.>
```

The placeholder form above is a shape reference only. Replace every placeholder before marking a
record complete. A real record may add sections, but it keeps the required sections co-located and
does not hide findings in a long undifferentiated timeline.

## Ledger rules

Each finding gets one stable ID such as `R1`. The row states an observation before its inference,
names evidence that another agent can inspect, and says what a tempting simplification would
break. The `Placement` cell names the primary source of truth; the map below may point to secondary
tests or records without duplicating the rationale. Public API coverage records the inventory and
the check used to establish completeness; it does not repeat each member's description.

Keep rejected approaches and failed checks when they explain the final shape. Record exact package
versions or commands when they are needed to reproduce a discovery; let manifests, lockfiles, and
CI remain authoritative for values that can change independently.

## Verification and closure

Verification records the command, expected/selected targets, environment, result, skips, and
limitation. New/materially changed critical gates need valid/violation fixture evidence or
a pending effectiveness check. Format validation proves neither API coverage nor behavior.
A command that was
not run is `not-run` with a prerequisite or owner; an unavailable dependency or permission is
`blocked`. "Tests passed" without the command or scope is not a verification record.

The record is `complete` only when:

- every ledger ID has exactly one primary placement;
- every comment and sensor map row points to an existing source, test, record, or command;
- when the public API coverage section is present, every listed surface has a documented scope and
  a stated coverage check;
- design drift is resolved, linked to a new decision, or explicitly owned and deferred;
- verification states reflect what actually ran; and
- remaining boundaries are visible to the next implementer.
