# Structure Review contract

Use this contract for the durable output of a repository-structure investigation. If
the repository already has an Architecture Brief or ADR format, add or link these
fields there instead of creating a competing document.

## Placement and lifecycle

Follow the repository's documentation convention. When none exists, use
`docs/architecture/briefs/structure-<slug>.md` for the review and the repository's ADR
location for a durable choice. A read-only audit may stay in the response when no record
was authorized.

Use one review status:

- `draft` - mapping or evidence is incomplete;
- `in-review` - candidates are ready for a decision;
- `accepted` - the selected structure and sensors are approved;
- `superseded` - a later review owns the structure decision;
- `blocked` - a required boundary or authorization is unavailable.

Use `confirmed`, `inferred`, `unknown`, `not-run`, and `blocked` for evidence and sensor
rows. A threshold crossing is an observed signal, not proof that a migration is needed.

## Required shape

```markdown
# Structure Review: <slug>

Status: draft
Date: YYYY-MM-DD
Owner: <person or team>
Authorization: design | probe | record | migrate

## Objective
<The navigation, ownership, dependency, or evolution outcome.>

## Non-goals
<Behavior, public API, build, release, or unrelated cleanup outside scope.>

## Baseline
<Branch and SHA, protected changes, relevant repository rules, target roots,
current tree, and existing local/global documentation.>

## Structure Map
| ID | Path/glob | Purpose and non-goals | Owner | Entry/visibility | Allowed dependencies | Consumers/lifecycle | README |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | `<path>` | <responsibility> | <owner> | <entry or private> | <boundary IDs> | <consumers/lifecycle> | present/missing/not-warranted |

## Signals
| ID | Path | Signal | Threshold/baseline | Observation | Evidence | State | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | `<path>` | direct production files | review at 12 | <value> | <command/report> | confirmed | retain/document/review/migrate/waive |

## Boundary README coverage
| Boundary | Local context | Reason | Parent/global link | Validation | State |
| --- | --- | --- | --- | --- | --- |
| B1 | `README.md` | <why it is or is not warranted> | <link> | <check> | confirmed |

## Candidates
### C0 - Current or smallest safe change
<Layout, local context, sensors, consequences, and growth path.>

### C1 - <alternative>
<Layout, boundaries, allowed dependency direction, and consequences.>

### C2 - <alternative when materially different>
<Package/build/visibility/ownership implications and consequences.>

## Decision
Selected candidate: <C0/C1/C2 or deferred>
<Rationale, sensitivity points, and revisit trigger.>

## Sensors
| ID | Invariant | Check/report | Cadence | Owner | State | Failure action | Waiver/expiry |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | <property> | <native check> | <when> | <owner> | confirmed | <repair> | none |

## Migration and rollback
<Exact path phases, reference and metadata updates, compatibility window,
verification, rollback point, and commit-plan handoff.>

## Open questions
- <question> - owner: <owner>; next check: <action>; state: unknown
```

Replace every placeholder before accepting the record. Use `None - <reason>` for an
inapplicable section. Link to a canonical Architecture Brief, ADR, ownership file, build
configuration, or local README instead of duplicating its facts.

## Map rules

The Map is complete only when:

- every path discovered by the scoped inventory belongs to a component or explicit container;
  inventory roots, exclusions, and unavailable sources are stated;
- each component has one primary responsibility and an owner or owned unknown;
- public entrypoints and private implementation paths are distinguishable;
- allowed dependency edges use stable boundary IDs rather than incidental filenames;
- tests, generated material, vendored material, documentation, and tooling are classified;
- local README coverage has a reason rather than a quota;
- cross-boundary edges and shared components have evidence and consumers;
- the tree and graph are described as separate views.

Report actual gate selection and pass/fail/skip outcomes for the mapped invariants. A file
count establishes only that count. A new/materially changed critical gate needs a valid
fixture and controlled violation proving detection, or an explicit pending check.

## Optional structure policy

Introduce a machine-readable policy only when a sensor needs stable repository-local
configuration. Follow an existing repository format when present. A minimal language-neutral
shape may contain:

```json
{
  "version": 1,
  "exclude": ["**/generated/**", "**/vendor/**"],
  "exclude_defaults": true,
  "thresholds": {
    "observe_direct_production_files": 8,
    "review_direct_production_files": 12,
    "compare_direct_production_files": 20
  },
  "boundaries": [
    {
      "id": "core",
      "path": "source/core",
      "owner": "team-or-person",
      "readme": "required",
      "allowed_dependencies": ["contracts"]
    }
  ],
  "waivers": []
}
```

This is a semantic contract, not a required filename or serialization format. Keep derived
file lists and commands in their executable sources of truth. A waiver records boundary ID,
signal, reason, owner, approval, expiry or revisit trigger, and the sensor that will re-open
the decision.

## Handoff gate

A fresh agent must be able to identify the current tree, real component boundaries, local
context, allowed edges, selected candidate, exact migration scope, verification state, and
next authorization without reconstructing hidden reasoning.
