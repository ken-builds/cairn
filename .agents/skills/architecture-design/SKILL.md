---
name: architecture-design
description: Design and review cross-module changes in an existing repository through global-model reconstruction, terminology control, evidence-backed research, isolated feasibility probes, and recorded architectural decisions.
---

# Architecture Design

Use this skill when a requirement or bug fix crosses module boundaries, changes a public
contract, introduces or upgrades a dependency, changes data or runtime topology, or has
meaningful performance, reliability, security, or migration risk. It is for architecture
work on an existing repository; ordinary local edits and greenfield system design stay
outside the default path.

## Operating contract

The deliverable is an evidence-backed design another agent can execute without guessing:
an Architecture Brief, one or more ADRs when a durable decision is made, and a response
summary that links to the repository records. Discover the repository's existing document
and ADR conventions first. When none exist, use `docs/architecture/briefs/` and
`docs/architecture/decisions/`.

Treat the workflow as three authorization levels:

- **design** — read the repository and, when allowed, consult external sources; keep the
  repository unchanged.
- **probe** — after explicit user authorization, use a disposable worktree or scratch
  project for dependency installation, PoCs, benchmarks, compatibility checks, fault
  injection, or formal models.
- **record** — after explicit user authorization, write the Brief and ADRs to the
  discovered documentation location. Product-code implementation remains a separate
  request unless the user explicitly includes it.

State the active level and any missing authorization in the first update. A read-only
plan, unavailable network, or unavailable tool produces `unknown`, `not-run`, or
`blocked` evidence with the next safe action; it never becomes a claimed validation.

Keep these leading words stable throughout the work:

- **baseline** — the starting repository state, scope, and protected changes.
- **Map** — the evidence-backed global model of modules, flows, contracts, data, runtime,
  and ownership.
- **Glossary** — the canonical terminology ledger, including scope and aliases.
- **driver** — a requirement or quality scenario that can distinguish candidates.
- **candidate** — a concrete design option, including the no-change baseline.
- **evidence** — a sourced fact or measured observation, separated from inference.
- **probe** — a bounded experiment that tests a named assumption.
- **sensor** — an executable or observable check that detects architectural drift.
- **decision** — one durable choice recorded in one ADR.
- **drift** — divergence discovered after a design or implementation changes the system.

Use the state labels `confirmed`, `inferred`, `unknown`, `not-run`, and `blocked` for
claims, probes, and sensors. Keep one authoritative definition for each term and one
authoritative rationale for each decision.

## Conditional references

Read only the references that the current branch reaches:

- Read [reading-map.md](references/reading-map.md) when selecting an architecture lens,
  notation, or source; it is a routing map, not a reading assignment.
- Read [evidence-research.md](references/evidence-research.md) when a framework, library,
  protocol, version, vulnerability, compatibility promise, or current best practice can
  affect the decision.
- Read [probe-and-benchmark.md](references/probe-and-benchmark.md) when a performance,
  concurrency, failure, compatibility, capacity, data-structure, or feasibility unknown
  could change the candidate ranking.
- Read [artifact-contract.md](references/artifact-contract.md) before writing or validating
  an Architecture Brief, ADR, Evidence record, Probe record, or Sensor record.

## Workflow

### 1. Establish the baseline

1. Read repository-local instructions and sources of truth in this order: `AGENTS.md` or
   `CLAUDE.md`, contribution docs, build and test scripts, manifests and lockfiles, CI,
   deployment configuration, architecture docs, and existing ADRs.
2. Capture the current branch, `HEAD`, index/worktree status, untracked paths, and any
   pre-existing or protected changes. Identify the requested outcome, explicit non-goals,
   affected environments, and the authorization level.
3. Separate repository facts, user constraints, assumptions, and open questions. Give
   every open question an owner or a safe stopping condition.

**Done when:** the baseline records the scope, protected state, relevant rule sources,
and every plausible affected subsystem; unresolved boundaries are visible rather than
silently assigned.

### 2. Build the Map before proposing a patch

1. Trace the relevant entrypoints and end-to-end flows through callers, modules, storage,
   queues, external services, configuration, deployment, and observability. Inspect actual
   code and generated/configured wiring instead of inferring from directory names.
2. Inventory public APIs, schemas, events, persistence ownership, error and retry
   semantics, consistency assumptions, lifecycle boundaries, and tests that exercise the
   path. Record both upstream consumers and downstream effects.
3. Choose the smallest useful set of views. C4 levels and ISO 42010 terms may organize the
   description; they are communication aids, not proof that the design is sound.
4. Mark each statement as evidence-backed or unknown, and link it to a file, symbol,
   command, test, or runtime observation.

**Done when:** every proposed touch point has a Map entry with its boundary, consumers,
producers, invariants, operational path, and evidence; every missing fact is listed as an
unknown with a plan to resolve it.

### 3. Rebuild the Glossary

1. Search the repository for each domain noun, type, field, endpoint, event, and layer
   name before introducing terminology. Include docs, schemas, tests, logs, metrics, and
   configuration keys.
2. Record the canonical term, scope or bounded context, definition, source location,
   known aliases, and relationships to neighboring concepts. Keep identical concepts
   under one term; keep genuinely different concepts distinct even when their names match.
3. Make a new term earn its place: show why an existing term is insufficient, define the
   new scope, and state the migration or alias policy. Flag overloaded words and cross-layer
   collisions for review.

**Done when:** every noun used by a candidate maps to one Glossary entry, every alias has
an owner and retirement status, and no unexplained synonym or hierarchy collision remains.

### 4. Turn goals into drivers and scenarios

1. Convert the request into functional drivers and only the quality attributes that can
   affect the choice. Include security, operability, cost, deployability, and migration
   constraints when they are real drivers.
2. Write each important scenario with a stimulus, context, response, metric, threshold,
   priority, and failure meaning. State the failure model and consistency or compatibility
   semantics instead of using labels such as “scalable” or “reliable” alone.
3. Identify conflicts between drivers and rank them with the user or repository policy.
   A driver without an observable test is an assumption, not an evaluation criterion.

**Done when:** every candidate will be compared against a finite set of observable,
prioritized scenarios and every hard constraint has an explicit pass/fail interpretation.

### 5. Form and compare candidates

1. Keep the current design or smallest safe change as the baseline candidate. Add at least
   one materially different candidate for a low-risk change; add two viable alternatives
   for cross-boundary, runtime, migration, or high-uncertainty work.
2. For each candidate, describe ownership and information hiding, interfaces and data
   flow, coupling and complexity, failure propagation, security boundaries, operations,
   migration and rollback, dependency implications, and likely drift sensors.
3. Use the drivers to make trade-offs explicit. Distinguish measured evidence, sourced
   facts, inference, and unknowns. Use a named pattern only when it explains a required
   property; the pattern name never substitutes for the property.
4. Identify sensitivity points, risks, and reversible choices. Select a candidate only
   after stating what would change the selection.

**Done when:** the candidate comparison covers the relevant drivers and boundaries, the
selected option has a one-sentence decision rationale, and every material unknown is either
assigned to Evidence/Probe or accepted as a documented risk.

### 6. Pass the Evidence gate when facts can change

Read [evidence-research.md](references/evidence-research.md) for this step.

1. Treat framework, library, protocol, release, security, compatibility, and “current
   best practice” claims as time-sensitive. Query official documentation, release notes,
   issue/PR discussions, advisories, and fixing commits in that order; use secondary
   sources only to discover what to verify.
2. Record the exact claim, source URL, package/project, version or commit, access date,
   applicable environment, evidence state, and the inference (if any). Check the local
   manifest and lockfile against the researched version.
3. Prefer a supported upstream release containing the fix. Evaluate upgrade impact,
   compatibility, license, security, migration, and rollback before adopting it. Use a
   workaround, patch, or fork only when the upstream path is unavailable or unsafe, and
   record an owner, exit condition, and re-check date.
4. Bound the research. Stop when each decision-changing claim is confirmed, rejected, or
   explicitly marked unknown with a next query; do not turn an architecture task into an
   unbounded literature survey.

**Done when:** every dynamic claim in the Brief has a dated source and version/commit,
upstream repair options have been considered, and no remembered fact is presented as
current evidence.

### 7. Pass the Probe gate for decision-changing unknowns

Read [probe-and-benchmark.md](references/probe-and-benchmark.md) for this step.

1. Trigger a probe when a performance, concurrency, failure, compatibility, capacity,
   data-structure, algorithm, or integration assumption could reorder the candidates or
   change a hard constraint. Choose the smallest experiment that can discriminate them.
2. Existing read-only inspection and lightweight checks that leave the repository and
   external systems unchanged stay at the `design` level. Before creating or modifying
   experiment files, installing/upgrading dependencies, running load or fault injection,
   or otherwise mutating external state, obtain explicit user authorization for the
   `probe` level. Use a disposable worktree, temporary directory, or scratch project;
   keep credentials, production systems, and the real worktree outside the experiment.
3. Write the experiment card first: hypothesis, workload or input model, baseline,
   environment, method, success threshold, sample/timeout budget, and cleanup plan. Run
   a baseline and the candidate under comparable conditions.
4. For benchmarks, report warm-up, repetitions, p50/p95/p99 or another justified
   distribution, errors, utilization/saturation, variance, and measurement limitations.
   For failure or compatibility probes, report the injected condition, observed response,
   recovery, and residual risk. Use formal methods or property-based tests only when the
   concrete invariant justifies their cost.
5. Preserve the result and commands, clean disposable state, and feed the result back
   into the candidate matrix. A compile-only spike is feasibility evidence, not a quality
   guarantee.

**Done when:** each decision-changing unknown has a confirmed probe result or a clearly
marked not-run/blocked record with the exact authorization or prerequisite needed next.

### 8. Record the decision and handoff

Read [artifact-contract.md](references/artifact-contract.md) before creating files.

1. Discover the repository's document location. If none exists, use
   `docs/architecture/briefs/` for the exploratory Brief and
   `docs/architecture/decisions/` for one ADR per durable decision.
2. After explicit `record` authorization, write the Brief with the Map, Glossary, drivers,
   candidates, Evidence, Probes, Sensors, decision, and open questions. Keep rationale in
   the ADR as the authoritative decision record; link rather than duplicate it.
3. Give each ADR a status, context, decision, alternatives, evidence, consequences,
   confidence, revisit trigger, and supersession links. An accepted decision evolves via
   a new superseding ADR; preserve its historical rationale.
4. State migration phases, compatibility windows, rollback effects, ownership, and the
   first implementation checkpoint. Separate selected work from deferred or explicitly
   rejected work.

**Done when:** a fresh agent can identify the chosen candidate, exact boundaries, evidence,
experiment status, migration/rollback sequence, and unresolved decisions from the linked
records without reconstructing hidden reasoning.

### 9. Encode Sensors and check Drift

1. Turn each critical invariant into the cheapest useful sensor: dependency-direction
   rule, structural test, API/schema contract, compatibility check, benchmark budget,
   property test, security check, metric, trace, or operational alert. Give failures a
   repair path and an owner.
2. Re-run relevant checks after the design or implementation changes the Map. Compare the
   resulting terminology, boundaries, contracts, dependencies, and runtime assumptions
   with the Brief and ADR.
3. Record drift as a new decision or superseding ADR when the intended architecture
   changes. Update the Glossary and Map at their source of truth; keep the response summary
   concise and linked.

**Done when:** every critical invariant has a passing sensor or an explicit owner and
waiver, the post-change Map agrees with reality, and the final summary distinguishes
confirmed, inferred, unknown, not-run, and blocked work.

## Response handoff

End with a compact summary containing: scope and status, links to the Brief/ADRs, selected
candidate, key trade-offs, Evidence and Probe states, Sensors, migration/rollback, open
decisions, and the next authorization needed. The repository records are the long-lived
source of truth; the response is an index, not a second architecture document.
