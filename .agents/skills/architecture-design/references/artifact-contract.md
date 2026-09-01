# Architecture artifact contract

Use this file as the single source of truth for the files produced by the architecture
workflow. The response is an index; it does not replace these records. Adapt labels to the
repository's established style while retaining the required meaning and status.

## Status and evidence vocabulary

Use one status per artifact:

- Brief: `draft`, `in-review`, `accepted`, `superseded`, or `blocked`.
- ADR: `proposed`, `accepted`, `rejected`, `superseded`, or `deprecated`.
- Evidence, Probe, and Sensor: `confirmed`, `inferred`, `unknown`, `not-run`, or `blocked`.

These labels are claims about the record, not decoration. `not-run` means a command did not
run; `blocked` means a safety, access, or environment constraint stopped it; neither means
pass. `inferred` identifies reasoning that still depends on an assumption. The lifecycle
status of a Brief or ADR is independent from the row-level state of its Evidence, Probes,
and Sensors; report both when they differ.

## Architecture Brief

Use one Brief per coherent design investigation. It is the exploration and handoff record;
the ADR is the authoritative record for each durable choice.

Required shape:

```markdown
# Architecture Brief: <slug>

Status: draft
Date: YYYY-MM-DD
Owner: <person or team>

## Objective
<desired outcome and success boundary>

## Non-goals
<explicitly deferred or out-of-scope behavior>

## Baseline
<HEAD/branch, relevant repository rules, protected changes, and authorization>

## Map
<modules, entrypoints, flows, contracts, data ownership, runtime/deployment,
observability, and evidence links>

## Glossary
| Term | Scope | Canonical meaning | Source | Aliases/relations |
| --- | --- | --- | --- | --- |
| <term> | <context/layer> | <meaning> | <path or URL> | <aliases or none> |

## Drivers and scenarios
| ID | Stimulus | Context | Response | Metric | Threshold | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | <stimulus> | <context> | <response> | <metric> | <threshold> | P0 |

## Candidates
### C0 — Current or smallest safe change
<boundary, data flow, consequences, and trade-offs>

### C1 — <alternative>
<boundary, data flow, consequences, and trade-offs>

### C2 — <alternative, when the risk profile calls for another viable option>
<boundary, data flow, consequences, and trade-offs>

## Evidence
| ID | Claim | Source | Version/commit | Accessed/measured | State | Applicability |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | <claim> | <URL/path/command> | <version or SHA> | YYYY-MM-DD | confirmed | <scope> |

## Probes
| ID | Question | Hypothesis | Baseline | Threshold | Result | State | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | <question> | <hypothesis> | <baseline> | <threshold> | <result> | not-run | <link> |

## Decision
<selected candidate and link to the ADR; state what would change the selection>

## Sensors
| ID | Invariant | Check or signal | Frequency | Owner | State | Repair path |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | <invariant> | <test/rule/metric> | <when> | <owner> | confirmed | <action> |

## Migration and rollback
<phases, compatibility window, rollout, rollback effect, and first checkpoint>

## Open questions
- <question> — owner: <owner>; next check: <command/source/date>; state: unknown
```

The Map and Glossary may link to existing repository records instead of copying them. Keep
the Brief's table rows traceable to those sources. If a section has no applicable content,
write `None — not applicable because <reason>` rather than silently omitting the section.

## Architecture Decision Record

Use one ADR for one durable decision. Number and locate it according to repository
convention; when there is no convention, use `docs/architecture/decisions/ADR-<four-digit>-<slug>.md`.

Required shape:

```markdown
# ADR-<number>: <decision title>

Status: proposed
Date: YYYY-MM-DD
Deciders: <person or team>

## Context
<drivers, baseline, constraints, and links to the Brief>

## Decision
<one precise choice and its boundary>

## Alternatives
| Option | Why considered | Why not selected |
| --- | --- | --- |
| <option> | <fit> | <trade-off> |

## Evidence
- E1 — <claim, source/version/date, and link to Brief or probe>

## Consequences
### Benefits
- <benefit tied to a driver>
### Costs and risks
- <cost, risk, or accepted unknown>

## Confidence
<high/medium/low with the evidence and remaining assumptions>

## Revisit Trigger
<observable event, threshold, date, version, or assumption that requires review>

## Supersedes
<ADR link or None>

## Superseded by
<ADR link or None>

## Migration and rollback
<phases, compatibility, owner, checkpoint, and rollback effect>
```

An accepted ADR remains historical. Change its status only for a clear lifecycle event;
record a new ADR with `Supersedes` when the decision changes.

## Evidence, Probe, and Sensor records

Use these fields when a table row needs more detail than the Brief can hold.

### Evidence

```text
ID: E<id>
Claim: <precise, falsifiable statement>
Source: <URL, path/symbol, command, or artifact>
Project/package: <name>
Version or commit: <exact value>
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
Baseline: <current behavior/measurement>
Method and budget: <commands, warm-up, repetitions, timeout/cost>
Threshold: <driver-linked pass/fail rule>
Result and artifact: <observation and link>
State: confirmed | inferred | unknown | not-run | blocked
Limitations: <known confounders>
Cleanup: <what happened>
Follow-up: <decision or next check>
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

The final response should link the Brief and ADRs and summarize their statuses. It may
repeat the selected candidate and next action, but it should not create a competing glossary,
decision rationale, or set of thresholds. A new agent should be able to start from the
links, follow the evidence and probe artifacts, and identify the next authorized operation.
