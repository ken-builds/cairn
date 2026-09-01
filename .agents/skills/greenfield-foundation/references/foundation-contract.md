# Greenfield foundation artifact contract

Use this file as the single source of truth for the records produced by
`greenfield-foundation`. The response is an index; it does not replace these records. Adapt
labels to an established target-project convention while retaining the required meaning and
state vocabulary.

## Status and evidence vocabulary

Use one lifecycle status per artifact:

- Foundation Brief: `draft`, `in-review`, `accepted`, `superseded`, or `blocked`.
- ADR: `proposed`, `accepted`, `rejected`, `superseded`, or `deprecated`.
- Assumption, Evidence, Probe, and Sensor: `confirmed`, `inferred`, `unknown`, `not-run`, or
  `blocked`.

These labels are claims about the record. `not-run` means a check did not run; `blocked` means a
safety, access, authorization, or environment constraint stopped it. Neither label means pass.
Keep state cells machine-readable: start with one enum value. A short annotation may follow after
punctuation such as `—`, `;`, or parentheses; put longer rationale in the adjacent evidence,
owner, or follow-up field.

## Foundation Brief

Use one Foundation Brief per coherent greenfield initiative. It is the exploration and
implementation handoff record; an ADR is the authoritative record for each durable choice.

### Required metadata

```text
# Foundation Brief: <slug>

Status: draft
Date: YYYY-MM-DD
Owner: <person or team>
```

The title must identify the artifact as a `Foundation Brief`. Replace every angle-bracket
placeholder before recording the document.

### Required sections

The following headings are required. A heading may contain a table, prose, or subsections, but it
must contain meaningful content or an explicit `None — not applicable because ...` explanation.

```markdown
## Objective
## Non-goals
## Mandate and baseline
## Constraints and assumptions
## Context Map
## Glossary
## Drivers and scenarios
## Candidates
## Foundation Blueprint
## Evidence
## Probes
## Decision
## Bootstrap plan and gates
## Walking skeleton / first vertical slice
## Sensors and Definition of Done
## Evolution and rollback
## Open questions
```

### Minimum content by section

| Section | Minimum contract |
| --- | --- |
| Objective | Desired outcome and the boundary at which the design is useful. |
| Non-goals | Explicitly deferred behavior, systems, or implementation work. |
| Mandate and baseline | Mission, users/stakeholders, supplied material, target environments, ownership, authorization, and any protected early-repository state. |
| Constraints and assumptions | A ledger with `ID`, assumption/constraint, impact if false, validation or owner, and state. |
| Context Map | Actors, journeys, external systems, bounded contexts, trust boundaries, data owners, and target deployment/ownership views. |
| Glossary | Canonical `Term`, `Scope`, `Canonical meaning`, `Source`, and `Aliases/relations` columns. |
| Drivers and scenarios | A row for each material scenario with `ID`, `Stimulus`, `Context`, `Response`, `Metric`, `Threshold`, and `Priority`. |
| Candidates | At least the smallest reversible C0 and any materially different alternatives; record fit, trade-offs, reversibility, and state. |
| Foundation Blueprint | A concern matrix covering boundaries, dependency direction, interfaces/contracts, data ownership, runtime/deployment, security/trust, observability, delivery/release, and cost/capacity. |
| Evidence | Decision-changing claims with source, version/commit, access date, environment, state, applicability, and inference. |
| Probes | Decision-changing experiments with question, hypothesis, workload/input, environment, baseline, method/budget, threshold, result, state, limitations, cleanup, and follow-up. `None` is valid when no probe is needed. |
| Decision | The selected candidate, one-sentence rationale, sensitivity points, ADR links, and deferred/rejected choices. |
| Bootstrap plan and gates | Ordered G0–G4 stages, entry conditions, deliverables, exit criteria, owners, and state. |
| Walking skeleton / first vertical slice | One concrete end-to-end path and its contract, data, test, deploy, observe, rollback, and acceptance path. |
| Sensors and Definition of Done | Critical invariants, checks/signals, cadence, owner, state, failure action, and the minimum handoff completion bar. |
| Evolution and rollback | Release phases, reversible boundaries, data initialization, rollback effect, and the first implementation checkpoint; explain why migration is not applicable when there is no predecessor. |
| Open questions | Each question has an owner, next check, and state, or the section contains an explicit None reason. |

### Foundation Brief template

```markdown
# Foundation Brief: <slug>

Status: draft
Date: YYYY-MM-DD
Owner: <person or team>

## Objective
<desired outcome and success boundary>

## Non-goals
<explicitly deferred work>

## Mandate and baseline
<mission, users, stakeholders, supplied material, target environments, ownership, authorization>

## Constraints and assumptions
| ID | Constraint or assumption | Impact if false | Validation/owner | State |
| --- | --- | --- | --- | --- |
| A1 | <assumption> | <impact> | <owner and next check> | unknown |

## Context Map
<actors, journeys, external systems, bounded contexts, trust boundaries, ownership, and deployment views>

## Glossary
| Term | Scope | Canonical meaning | Source | Aliases/relations |
| --- | --- | --- | --- | --- |
| <term> | <scope> | <meaning> | <source> | <aliases or none> |

## Drivers and scenarios
| ID | Stimulus | Context | Response | Metric | Threshold | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | <stimulus> | <context> | <response> | <metric> | <threshold> | P0 |

## Candidates
| ID | Option | Fit | Trade-offs | Reversibility | State |
| --- | --- | --- | --- | --- | --- |
| C0 | <smallest reversible foundation> | <fit> | <trade-offs> | <how to undo or defer> | inferred |

## Foundation Blueprint
| Concern | Target shape | Owner | Evidence/state |
| --- | --- | --- | --- |
| Boundaries | <modules/containers and responsibilities> | <owner> | <state> |
| Dependency direction | <allowed direction and rule> | <owner> | <state> |
| Interfaces/contracts | <API/event/schema and versioning> | <owner> | <state> |
| Data ownership | <source of truth and consistency> | <owner> | <state> |
| Runtime/deployment | <environments and topology> | <owner> | <state> |
| Security/trust | <identity, authorization, trust boundaries> | <owner> | <state> |
| Observability | <logs, metrics, traces, alerts> | <owner> | <state> |
| Delivery/release | <CI, deployment, rollback> | <owner> | <state> |
| Cost/capacity | <envelope and assumptions> | <owner> | <state> |

## Evidence
| ID | Claim | Source | Version/commit | Accessed/measured | State | Applicability |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | <claim> | <URL/path/command> | <version or SHA> | YYYY-MM-DD | confirmed | <scope> |

## Probes
| ID | Question | Hypothesis | Workload/input | Environment | Baseline | Method/budget | Threshold | Result | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | <question> | <hypothesis> | <input> | <environment> | <baseline> | <method and budget> | <driver threshold> | <result or None> | not-run |

## Decision
Selected candidate: <C0/C1/C2>

Rationale: <one sentence tied to the highest-priority drivers>

Sensitivity points: <what would change the selection>

ADR links: <links or None>

Deferred/rejected: <choices intentionally left out>

## Bootstrap plan and gates
| Gate | Entry | Deliverables | Exit criterion | Owner | State |
| --- | --- | --- | --- | --- | --- |
| G0 Mandate | <entry> | <deliverables> | <checkable exit> | <owner> | confirmed |

## Walking skeleton / first vertical slice
| Step | Boundary crossed | Test/observation | Deploy/rollback | Acceptance |
| --- | --- | --- | --- | --- |
| <step> | <boundary> | <check> | <path> | <criterion> |

## Sensors and Definition of Done
| ID | Invariant | Check or signal | When | Owner | State | Failure action |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | <invariant> | <check> | <local/CI/release/runtime> | <owner> | confirmed | <repair path> |

Definition of Done: <all required records, gates, slice, sensors, and open-question ownership>

## Evolution and rollback
<release phases, compatibility window, data initialization, rollback effect, first checkpoint>

## Open questions
- <question> — owner: <owner>; next check: <command/source/date>; state: unknown
```

## Architecture Decision Record

Use one ADR for one durable, revisitable decision such as an architecture style, boundary,
storage model, integration mode, security boundary, or external dependency. Keep local details in
the Brief unless they have an independent revisit trigger.

```markdown
# ADR-<four-digit>: <decision title>

Status: proposed
Date: YYYY-MM-DD
Deciders: <person or team>

## Context
<mandate, drivers, constraints, assumptions, and Foundation Brief link>

## Decision
<one precise choice and its boundary>

## Alternatives
| Option | Why considered | Why not selected |
| --- | --- | --- |
| <option> | <fit> | <trade-off> |

## Evidence
- E1 — <claim, source/version/date, and link to the Brief or probe>

## Consequences
### Benefits
- <benefit tied to a driver>
### Costs and risks
- <cost, risk, or accepted unknown>

## Confidence
<high/medium/low with evidence and remaining assumptions>

## Revisit Trigger
<observable event, threshold, date, version, or assumption>

## Supersedes
<ADR link or None>

## Superseded by
<ADR link or None>

## Migration and rollback
<greenfield release/evolution phases, compatibility, checkpoint, and rollback effect>
```

## Detailed evidence, probe, and sensor records

When a Brief table cannot carry the necessary detail, use the following fields in a linked record.

### Evidence

```text
ID: E<id>
Claim: <precise, falsifiable statement>
Source: <official URL, path/symbol, command, or artifact>
Project/package: <name>
Version or commit: <exact value or not stated>
Accessed/measured: YYYY-MM-DD
Environment: <scope>
State: confirmed | inferred | unknown | not-run | blocked
Applicability: <why it applies>
Inference: <reasoning or none>
Next check: <owner and action>
```

### Probe

```text
ID: P<id>
Question: <decision-changing question>
Hypothesis: <falsifiable statement>
Workload/input: <shape and scale>
Environment: <runtime, platform, versions, configuration>
Baseline: <current or reference behavior>
Method and budget: <commands, warm-up, repetitions, timeout/cost>
Threshold: <driver-linked pass/fail rule>
Result and artifact: <observation and link>
State: confirmed | inferred | unknown | not-run | blocked
Limitations: <known confounders>
Cleanup: <what happened>
Follow-up: <decision, sensor, or next experiment>
```

### Sensor

```text
ID: S<id>
Invariant: <property that must remain true>
Check or signal: <test, static rule, contract, benchmark, metric, trace, or alert>
When: <local/CI/release/runtime cadence>
Owner: <person/team>
State: confirmed | inferred | unknown | not-run | blocked
Failure action: <specific repair path>
Waiver/expiry: <if applicable>
```

## Handoff rules

The selected candidate and rationale live in the ADR; the Brief links to it and carries the full
Map, gate plan, slice, sensors, and open questions. A greenfield Brief may state that migration is
not applicable, but it must still describe release evolution and rollback. Once implementation
creates stable boundaries, keep the Brief historical and use a new or superseding ADR for drift.

The validator is a structural gate, not an architecture reviewer. A passing document still needs
human or agent review of actor/journey meaning, ownership, failure semantics, evidence quality,
conditional defaults, and whether the slice genuinely crosses the stated boundaries.
