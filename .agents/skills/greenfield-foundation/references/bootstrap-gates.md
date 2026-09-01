# Bootstrap gates and implementation handoff

This reference defines the staged foundation path. It is deliberately design-first: the gates
describe what an implementation team must be able to build and verify, while this skill only
records the blueprint and the checks. A gate is complete only when its exit criterion is
observable and its unresolved work has an owner.

## Gate sequence

| Gate | Purpose | Required outputs | Exit criterion |
| --- | --- | --- | --- |
| G0 Mandate | Establish why the system exists and what is constrained. | Objective, users/stakeholders, outcomes, non-goals, environments, ownership, budget/time, security/compliance constraints, assumption ledger. | A reader can state the success boundary and name every material constraint and assumption. |
| G1 Context and boundaries | Establish what the system and its neighbors own. | User journeys, Context Map, Glossary, actors, external systems, trust boundaries, data ownership, prioritized drivers. | Every important concept and boundary has a canonical owner, contract direction, and scenario impact. |
| G2 Blueprint and decisions | Choose a smallest viable and reversible target shape. | Candidate matrix, selected blueprint, dependency rules, interface/data/runtime/security/operations decisions, ADR links. | Hard drivers have thresholds; the selected candidate and the conditions that would overturn it are explicit. |
| G3 Walking skeleton | Prove that the design can carry one real outcome end to end. | First slice, contract and schema path, data lifecycle, test strategy, deploy/config path, observability, rollback, decision-changing probe cards/results. | One concrete stimulus can be traced across every important boundary to an observable acceptance result. |
| G4 Handoff | Make implementation sequencing and ownership unambiguous. | Foundation Brief, ADRs, ordered increments, Definition of Ready/Done, sensors, open-question ledger, next authorization. | A fresh implementer can start the first increment without inventing a cross-cutting rule or hiding an unknown. |

Do not advance a gate merely because its document section exists. An empty table, an unowned
assumption, or a threshold stated as “fast” is an incomplete exit.

## Definition of Ready

An increment is ready to implement when:

- its user or system outcome and acceptance signal are named;
- the owning boundary and its consumers/producers are in the Map;
- inputs, outputs, errors, idempotency, authorization, and data ownership are specified;
- dependencies and configuration/secret needs are identified;
- the test, deployment, observability, and rollback path is stated;
- unresolved assumptions are either outside the increment or assigned to a bounded probe;
- the increment does not silently introduce a new public term or boundary.

## Definition of Done for the foundation design

The foundation design is handoff-ready when:

- all required Foundation Brief sections pass the structural validator;
- every hard driver has a threshold and a selected-candidate comparison;
- every durable choice has an ADR or an explicit reason it remains reversible;
- the first slice crosses the real boundaries and names test/deploy/observe/rollback checks;
- every gate has an owner and an exit state;
- critical invariants have sensors with repair paths;
- open questions have owners and next checks, or a documented None reason;
- no `unknown`, `not-run`, or `blocked` item is presented as confirmed.

This is a design handoff, not a claim that code, infrastructure, or production readiness exists.

## Walking skeleton card

Use one card for the first slice. Keep it small enough to run repeatedly, but real enough to
exercise the boundaries that could invalidate the architecture.

```text
Slice: <short name>
User/system outcome: <observable outcome>
Stimulus: <request, event, schedule, or operator action>
Boundaries crossed: <ordered contexts/modules/services>
Contract path: <API/event/schema and version>
Data path: <owner, writes, reads, consistency, initialization>
Failure path: <timeouts, retries, duplicates, degradation, recovery>
Security path: <identity, authorization, trust transitions, audit>
Test path: <unit/contract/integration/system checks>
Deploy path: <environment, configuration, health, rollback>
Observe path: <logs, metrics, traces, alerts and owners>
Acceptance: <metric and threshold>
Unknowns/probes: <IDs or None>
```

If the slice cannot be described without hand-waving a boundary, return to G1 or G2. If a probe
requires mutation, obtain `probe` authorization and isolate it before running it.

## Ordered bootstrap plan

The handoff should turn the gates into a dependency-ordered implementation backlog:

1. establish repository and toolchain contracts;
2. enforce module/dependency boundaries and shared conventions;
3. implement the smallest contract and data path for the walking skeleton;
4. add automated checks, health signals, logs, metrics, and deployment verification;
5. expand capabilities one vertical slice at a time, revisiting ADRs only on a trigger.

Keep the first increment reversible. Defer optimization, extra deployables, secondary stores,
and platform generalization until a driver or measurement makes them necessary.

## Evolution and rollback

For a greenfield system, replace “migration from the old system” with explicit release evolution:

- identify the first release boundary and its compatibility promise;
- state how data is initialized, backed up, restored, or discarded;
- define how a bad deployment is rolled back without violating ownership or contracts;
- record the checkpoint that permits a later split, store replacement, or vendor exit;
- assign the owner and revisit trigger for each irreversible choice.

When there is no predecessor or persistent data yet, write `None — not applicable because ...` for
that part and still describe the initial release rollback effect.

## Handoff checklist

Before handing off, confirm:

- [ ] the target is still greenfield, or the next work has been routed to `architecture-design`;
- [ ] the selected candidate and all durable decisions link to the Brief and ADRs;
- [ ] the first slice has one observable acceptance path;
- [ ] implementation increments are ordered by real dependencies;
- [ ] test, deployment, observability, security, and rollback owners are named;
- [ ] unknowns, probes, waivers, and revisit triggers are visible;
- [ ] no product-code or infrastructure mutation was implied by the design record.
