---
name: greenfield-foundation
description: Design and record the initial architecture foundation for a new software system, from problem boundaries through a staged blueprint and first vertical slice; use for greenfield work, not established-repository evolution or product implementation.
---

# Greenfield Foundation

Use this skill to make a new software system ready for implementation without pretending that
unknown product, domain, or operational decisions are settled. The output is a durable,
evidence-backed Foundation Brief, ADRs for durable choices, and an implementation handoff.
The first version is design-first: it describes a repository and a walking skeleton but does not
create product code or mutate the target project. An authorized `probe` may install dependencies
or run a disposable experiment outside the target; provisioning and real releases remain outside
this skill.

## Boundary and operating contract

Use this skill when the project is new, empty, or still has no stable architecture boundary and
the user needs a foundation before feature implementation. It covers general software systems;
the selected stack may be web, mobile, data, platform, automation, or AI when the drivers require
it.

Hand off to `architecture-design` when the request is primarily a change to an established
repository: existing modules, public contracts, persistence, deployment, or runtime behavior are
the evidence to be evolved. Hand off to a technology-specific implementation skill when the
foundation is accepted and the user asks for code or infrastructure.

Classify ambiguous projects by what is relied upon: a disposable prototype, spike, or empty shell
whose boundaries and contracts are still being chosen remains greenfield; production consumers,
persistent data, operational commitments, or stable team-owned modules make it an evolution task.
If both are present, keep the new boundary decisions here and route changes to the established
part to `architecture-design`.

The deliverable is a Foundation Brief, one or more ADRs when a durable decision is made, and a
compact response handoff. Discover the target project's document and ADR convention first; when
none exists, use `docs/architecture/briefs/` for `Foundation Brief` files and
`docs/architecture/decisions/` for `ADR-<four-digit>-<slug>.md`.

Work at one authorization level at a time:

- **design** — inspect supplied material and the target location read-only; build the model and
  plan. Keep the target unchanged.
- **probe** — after explicit authorization, run a bounded experiment in a disposable directory,
  scratch project, or isolated environment. Dependency installation, load tests, fault injection,
  and compatibility runs belong here.
- **record** — after explicit authorization, write the Foundation Brief and ADRs to the discovered
  documentation location. Product-code or infrastructure implementation remains a separate
  request.

State the active level and any missing authorization in the first update. A missing prerequisite
  produces `unknown`, `not-run`, or `blocked` evidence with a next check; it never becomes a
  claimed validation.

## Stable vocabulary and states

Keep these leading words stable throughout the work:

- **mandate** — the mission, users, outcomes, non-goals, ownership, and success boundary.
- **baseline** — the starting problem-space state, supplied material, target environments,
  constraints, assumptions, and protected changes (if an early repository exists).
- **Map** — the target domain, context, boundaries, flows, deployment, trust, data, and ownership
  model; it is a blueprint of intended structure, not a guess from folder names.
- **Glossary** — the canonical domain and architecture terminology ledger.
- **driver** — a requirement or quality scenario that can distinguish candidates.
- **candidate** — a concrete foundation option, including the smallest reversible starting point.
- **blueprint** — the selected target shape and its contracts, ownership, runtime, and operating
  rules.
- **gate** — a phase exit condition that must be observable before the next foundation phase.
- **slice** — the smallest end-to-end path that crosses the important boundaries.
- **evidence** — a sourced fact or measured observation, separated from inference.
- **probe** — a bounded experiment that tests a named assumption.
- **sensor** — an executable or observable check that detects foundation drift.
- **decision** — one durable choice recorded in one ADR.
- **drift** — divergence between the accepted blueprint and the system that is later built.

Use these states exactly for evidence, probes, sensors, and assumptions:
`confirmed`, `inferred`, `unknown`, `not-run`, and `blocked`.

## Conditional references

Read only the references reached by the current branch:

- Read [foundation-contract.md](references/foundation-contract.md) before drafting, recording,
  or validating a Foundation Brief or ADR.
- Read [decision-lenses.md](references/decision-lenses.md) when comparing architecture style,
  boundaries, data, integration, build-versus-buy, deployment, security, or operating choices.
- Read [bootstrap-gates.md](references/bootstrap-gates.md) when defining phase gates, a walking
  skeleton, Definition of Ready/Done, release evolution, or the implementation handoff.
- Read [evidence-and-probes.md](references/evidence-and-probes.md) when a dynamic external fact or
  decision-changing feasibility unknown can affect the candidate ranking.
- Use `$repository-structure` when the proposed repository layout, component README coverage,
  ownership map, or dependency boundaries need a focused structure review; keep the initial
  system mandate and foundation blueprint in this skill.
- After product-code implementation, use `$implementation-rationale` when available and
  implementation findings need public API documentation comments, source rationale, executable
  sensors, an implementation record, or drift reconciliation.

## Workflow

### 1. Establish the mandate and baseline

1. Inspect the target location and supplied material read-only. Decide whether it is genuinely
   greenfield, an empty shell, or an established system. If stable code boundaries already drive
   the request, stop this workflow and name the `architecture-design` handoff.
2. Record the mission, primary users and stakeholders, desired outcomes, explicit non-goals,
   affected environments, team ownership, delivery window, budget/cost ceiling, security and
   compliance constraints, and the current authorization level.
3. Start an assumption ledger. For each assumption, record the impact if false, an owner, a next
   validation, and its state.

**Done when:** the project boundary, mandate, non-goals, constraints, assumptions, protected
state, and authorization are visible in the baseline; no existing-system premise is hidden.

### 2. Build the target Map

1. Trace the intended user journeys and domain capabilities from stimulus to outcome. Identify
   actors, external systems, bounded contexts, trust boundaries, data owners, and team owners.
2. Sketch the smallest useful context/container/module/deployment views. For every boundary,
   state its responsibility, inbound and outbound contracts, failure behavior, lifecycle, and
   information it hides.
3. Mark each statement as a supplied fact, an inference, or an unknown. Do not turn a named
   framework, a fashionable pattern, or an empty directory into evidence.

**Done when:** every proposed boundary has an owner, purpose, consumer/producer relationship,
operational path, and explicit unknowns or evidence links.

### 3. Rebuild the Glossary and turn goals into drivers

1. Search supplied requirements, examples, schemas, APIs, and existing vocabulary before adding
   a term. Keep one canonical term per concept and record aliases, scope, and neighboring terms.
2. Convert business outcomes and real constraints into a finite set of prioritized scenarios.
   Include only quality attributes that can change the foundation choice: security, reliability,
   latency, capacity, cost, operability, delivery speed, compliance, or evolvability.
3. Give every important scenario a stimulus, context, response, metric, threshold, priority, and
   failure meaning. A label such as “scalable” is not a driver until it has an observable test.

**Done when:** every noun in the blueprint has a Glossary entry and every material driver has a
threshold that can distinguish at least two candidates.

### 4. Form and compare candidates

1. Keep **C0** as the smallest reversible foundation, not a fictitious current implementation.
   Add materially different candidates when a driver, runtime boundary, team topology, or
   uncertainty warrants them.
2. Compare only relevant dimensions: architecture style and module ownership, dependency
   direction, synchronous/asynchronous interaction, data ownership and storage, build-versus-buy,
   deployment/environment strategy, security boundaries, observability, cost, reversibility, and
   evolution path.
3. Use the defaults in [decision-lenses.md](references/decision-lenses.md) as hypotheses. Confirm,
   override, or defer each one with a driver and evidence; never let a named pattern substitute
   for a property or threshold.
4. State the sensitivity points: what fact, measurement, team change, or threshold would change
   the selected candidate.

**Done when:** the candidate matrix covers the decision-changing drivers, the selected option has
an explicit rationale, and every unresolved sensitivity has an owner or a probe plan.

### 5. Specify the foundation blueprint

Write the selected target shape at implementation-ready granularity without implementing it:

- module/container responsibilities and one-way dependency rules;
- API, event, and schema ownership, validation, versioning, compatibility, and error semantics;
- data ownership, consistency, lifecycle, retention, backup, and initialization assumptions;
- runtime topology, environments, configuration/secret boundaries, release strategy, and rollback;
- authentication/authorization, trust boundaries, threat or compliance obligations;
- logs, metrics, traces, health signals, alert ownership, and operational runbooks;
- reproducible development, test, CI, and deployment surfaces;
- expected cost/capacity envelope and the assumptions that need measurement;
- a proposed repository layout that makes the boundaries visible.

Keep each choice linked to a driver, evidence state, owner, and revisit trigger.

**Done when:** an implementer can create the initial project structure and public boundaries
without inventing a missing cross-cutting rule.

### 6. Design the bootstrap gates and walking skeleton

Read [bootstrap-gates.md](references/bootstrap-gates.md). Arrange the work through these gates:

- **G0 Mandate** — problem, users, outcomes, non-goals, constraints, owners, and assumptions;
- **G1 Context and boundaries** — Map, Glossary, trust/data ownership, and prioritized scenarios;
- **G2 Blueprint and decisions** — candidate comparison, selected blueprint, and ADR links;
- **G3 Walking skeleton** — one end-to-end slice with contract, data, test, deploy, observe, and
  rollback paths, plus probes for decision-changing unknowns;
- **G4 Handoff** — validated records, ordered implementation increments, Definition of Ready/Done,
  sensors, and open-question ownership.

Describe the slice; do not build it under this skill. A slice that cannot cross a real boundary
does not validate the foundation.

**Done when:** each gate has entry conditions, deliverables, an exit criterion, an owner, and a
state, and G3 names a concrete end-to-end acceptance path.

### 7. Pass the evidence and probe gates

Use [evidence-and-probes.md](references/evidence-and-probes.md):

1. Treat framework, library, protocol, release, security, compatibility, and current-practice
   claims as time-sensitive. Prefer official documentation, release notes, advisories, and
   upstream fixing records; record version and access date.
2. Trigger a probe only when its result could reorder candidates or change a hard constraint.
   Write the experiment card before running it, use a disposable boundary, pin the environment,
   set a budget and threshold, and preserve the result and cleanup.
3. Keep design inspection separate from probe mutation. If authorization or a prerequisite is
   absent, record `not-run` or `blocked` and the exact next action.

**Done when:** each decision-changing claim is confirmed, rejected by evidence, or explicitly
tracked as unknown/not-run/blocked with a concrete next check.

### 8. Record and hand off

1. After explicit `record` authorization, write the Foundation Brief and one ADR per durable,
   revisitable decision. Keep rationale authoritative in the ADR and link to it from the Brief.
2. Run `scripts/validate_foundation.py` against the records. Fix structural failures; do not
   weaken the contract to hide an unresolved architecture question.
3. Hand off the selected blueprint to the implementation owner. State what is selected, deferred,
   rejected, or still unknown, and which later skill owns the next mutation.

**Done when:** a fresh agent can follow the records to identify the selected candidate, exact
boundaries, first slice, gate order, validation state, rollback/evolution path, sensors, and
next authorized operation without reconstructing hidden reasoning.

### 9. Encode sensors and monitor drift

1. Turn each critical invariant into the cheapest useful sensor: dependency rule, contract test,
   schema check, compatibility test, benchmark budget, security check, metric, trace, or alert.
2. Give every sensor an owner, cadence, state, failure repair path, and waiver/expiry when needed.
3. When implementation changes the target Map or a boundary becomes established, record drift and
   continue the evolution work with `architecture-design` or the relevant implementation skill.

**Done when:** every critical invariant has a passing sensor or an explicit owner and waiver, and
the handoff distinguishes confirmed, inferred, unknown, not-run, and blocked work.

## Response handoff

End with a compact summary containing the scope and status, Foundation Brief/ADR links, selected
candidate, key trade-offs, evidence and probe states, gate status, sensors, evolution/rollback,
open questions, and the next authorization needed. The records are the long-lived source of
truth; the response is an index, not a second architecture document.
