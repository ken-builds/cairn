# Greenfield decision lenses

Use this reference when a foundation choice could alter a driver, a hard constraint, or the
shape of the first vertical slice. It is a routing map and a set of conditional starting
hypotheses, not a catalog of fashionable patterns. The project requirements, measured probes,
official product documentation, and team capability remain the evidence.

## Selection posture

Start with the driver, then ask which boundary hides the decision most likely to change. Record
the smallest option that satisfies the driver and keeps later choices reversible. For each default,
write the condition that would override it and the revisit trigger that would make it stale.

## Driver-to-lens map

| Driver signal | First lens | Questions to answer |
| --- | --- | --- |
| Unclear domain or overlapping nouns | domain and information hiding | What concept owns the rule? Which representation or policy should remain private? Which term is canonical? |
| Multiple stakeholders or views | architecture description | Which concerns need separate views? Which actor or team owns each boundary? |
| Competing quality goals | quality scenarios | What stimulus, metric, threshold, priority, and failure meaning distinguish the candidates? |
| Independent scaling, release, fault, security, or team ownership | boundary and deployment | Is a separate process/service justified, or is a module boundary enough for the first slice? |
| Long-running work, fan-out, retry, or temporal decoupling | interaction mode | What ordering, idempotency, delivery, and recovery semantics are required before using async messaging? |
| Transactional invariants or shared business state | data ownership | What is the single source of truth, who may write it, and what consistency is required? |
| High volume, search, analytics, or retention pressure | storage specialization | Is a second store necessary now, and what synchronization or rebuild path owns it? |
| Commodity capability or operational burden | build versus buy | Is the capability differentiating, privacy-sensitive, or control-sensitive enough to build? Who owns the vendor exit path? |
| Regional latency, availability, or regulatory placement | topology and recovery | What is the failure model, data residency rule, recovery objective, and rollback boundary? |
| Security or compliance exposure | trust and threat modeling | Where are identities, secrets, permissions, audit records, and trust transitions enforced? |
| Delivery speed or uncertain product shape | evolution and reversibility | Which decisions can be deferred behind a stable contract, and which must be fixed before the slice? |

## Conditional defaults

Treat these as C0 hypotheses. They are useful starting points for a general software system, not
universal requirements.

### Boundaries and architecture style

- For a proposed abstraction, name its consumer, contract owner, hidden variation, and concrete
  assembly point. Test a driver-motivated substitution: which parts change and which consumer
  behavior stays fixed? A test seam or trust boundary can justify separation without multiple
  implementations. Otherwise keep concrete code and a revisit trigger.
- Start with a modular monolith or the smallest number of deployable units that can express the
  real ownership boundaries.
- Split a process or service when independent release, scaling, security isolation, failure
  containment, data ownership, or team ownership is a measured or explicit driver.
- Keep dependency direction one-way toward stable policies and contracts. A convenience import
  that leaks a volatile implementation is a boundary failure, not a harmless shortcut.

### Interaction and data

- Use a synchronous request/response path for the first slice unless the driver requires temporal
  decoupling, long work, fan-out, buffering, or independent retry.
- Give each consistency boundary one authoritative owner. Add replicas, caches, search indexes,
  or event projections only with a freshness, scale, query, or availability requirement and an
  explicit rebuild/reconciliation path.
- Define idempotency, ordering, timeout, retry, and error semantics before introducing an async
  boundary. “Use a queue” is not an interaction contract.

### Build, buy, and dependencies

- Prefer a supported managed or purchased capability for undifferentiated operations when its
  security, license, data, cost, and exit constraints fit the drivers.
- Build when the capability is product differentiation or requires control, privacy, latency, or
  behavior unavailable from a supported option.
- Pin and record dependency versions, ownership, upgrade policy, license posture, and rollback
  path. A package name alone is not evidence of suitability.

### Runtime and operations

- Establish one reproducible development/test/release path before adding deployment variants.
- Make configuration and secrets explicit by environment; keep secret values out of records and
  command output.
- Include health, structured logs, useful metrics, traces where cross-boundary behavior needs them,
  and an owner for every alert before calling the foundation operationally ready.
- Add multi-region, multi-cluster, or elaborate platform layers only when availability, latency,
  residency, or isolation thresholds require them.

## Candidate comparison card

For candidates that survive the first screen, record the dimensions relevant to their drivers:

1. **Boundary** — what it owns, hides, and exposes.
2. **Flow** — how requests, events, data, and failures move through it.
3. **Drivers** — which scenarios it satisfies and at what threshold.
4. **Coupling** — compile-time, runtime, data, deployment, and team coupling introduced.
5. **Failure** — timeout, retry, duplication, degradation, recovery, and data-loss behavior.
6. **Security** — identity, authorization, trust transitions, secrets, and audit obligations.
7. **Operations** — deploy, observe, debug, scale, cost, and on-call burden.
8. **Evolution** — compatibility window, migration or replacement path, and rollback effect.
9. **Evidence** — confirmed facts, inferences, unknowns, and probes that could change the rank.
10. **Sensors** — the cheapest checks that will expose drift after implementation.

Do not rank candidates by pattern names, diagram aesthetics, or the number of components. Rank
them by driver satisfaction, explicit constraints, reversibility, and evidence quality.

## Decision stopping rule

Stop comparing when each hard driver has a pass/fail interpretation, the selected candidate wins
on the prioritized scenarios, remaining unknowns have an owner or a bounded probe, and another
candidate would win only if a named sensitivity point changes. Record that sensitivity in the ADR
instead of extending the survey indefinitely.
