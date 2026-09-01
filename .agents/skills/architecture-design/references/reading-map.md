# Architecture reading map

This file routes a design question to a useful lens. Load only the row or branch that
matches the current drivers. These sources supply vocabulary and heuristics; the
repository, measurements, and official product documentation remain the evidence for a
particular decision.

## How to choose a lens

Start with the driver, not with a favorite architecture style.

| Signal in the task | First lens | What to extract |
| --- | --- | --- |
| Repeated concepts, confusing names, leaky layers | abstraction and information hiding | canonical terms, hidden decisions, boundary ownership |
| Several stakeholders or views of the system | architecture description | concerns, viewpoints, context/container/component relationships |
| Competing quality goals | quality-attribute evaluation | scenarios, thresholds, sensitivity points, trade-offs |
| A durable choice or a choice likely to be revisited | decision records and evolution | context, alternatives, consequences, revisit trigger |
| Distributed state, data, or failure | data and reliability | consistency semantics, failure model, recovery and migration |
| A claim about latency, capacity, or feasibility | measurement and probing | workload, baseline, threshold, distribution, uncertainty |
| Existing code is hard to change safely | legacy and refactoring | characterization tests, seams, incremental migration |
| Team ownership or service boundaries affect the design | socio-technical design | communication paths, ownership, interaction modes |
| Agent behavior, feedback, or architecture drift | harness and sensors | feedforward guidance, feedback sensors, executable fitness |

## Stable cross-stack sources

Use these as a compact vocabulary, not as a reason to apply a pattern by name.

### Abstraction and modularity

- [SICP](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/)
  — abstraction barriers, composition, and representation independence. Use it when the
  design needs to recover concepts before adding code.
- [Parnas, On the Criteria To Be Used in Decomposing Systems into Modules](https://dl.acm.org/doi/10.1145/361598.361623)
  — information hiding and decomposition by likely change. Ask what decision a boundary
  hides and which changes its interface would force elsewhere.
- [Ousterhout, A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php)
  — complexity, deep modules, information leakage, and shallow wrappers. Treat these as
  review heuristics rather than universal laws.
- [Evans, Domain-Driven Design resources](https://www.domainlanguage.com/ddd/)
  — ubiquitous language, bounded contexts, and context mapping. Load for a genuinely
  complex domain; keep simple CRUD designs simple.
- [Brooks, No Silver Bullet](https://doi.org/10.1109/MC.1987.1663532)
  — essential versus accidental complexity. Use it to test whether a proposed framework
  change addresses the actual driver.
- [The Art of Unix Programming](http://www.catb.org/esr/writings/taoup/)
  — composition, transparency, separation of mechanism and policy, and replaceable tools.
  Use as a design attitude, not as a distributed-systems specification.
- [Fowler, Refactoring](https://martinfowler.com/books/refactoring.html)
  — behavior-preserving small steps. Pair with characterization tests when the current
  design is poorly understood.
- [Design Patterns](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
  — a shared vocabulary for recurring object-structure choices. Use it as a lookup for
  alternatives; a pattern name never establishes that its forces match this repository.

### Architecture description and communication

- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)
  — architecture description, stakeholders, concerns, viewpoints, and views. Verify the
  edition and use only the minimum vocabulary needed for the task.
- [C4 model](https://c4model.com/)
  — context, container, component, and code views. Use it to choose a useful map depth;
  a diagram is not an evaluation or a decision.
- [arc42](https://arc42.org/)
  — a practical docs-as-code outline. Select sections that answer current concerns;
  leave irrelevant sections out.
- [Rozanski and Woods viewpoints and perspectives](https://www.viewpoints-and-perspectives.info/)
  — stakeholder perspectives such as deployment, operations, security, data, and
  availability. Load when one diagram would hide an important concern.

### Quality attributes, trade-offs, and decisions

- [Software Architecture in Practice, 4e](https://www.sei.cmu.edu/library/software-architecture-in-practice-fourth-edition/)
  — quality attributes as architecture drivers and decisions as managed artifacts.
- [Fundamentals of Software Architecture](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/)
  and [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086895/)
  — trade-off vocabulary and distributed architecture decisions. Use their heuristics to
  frame a choice, then validate it against repository evidence and scenarios.
- [SEI Quality Attribute Workshop](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/)
  — elicit, refine, and prioritize scenarios before choosing a structure.
- [SEI ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/)
  — compare scenarios, sensitivity points, trade-off points, and risks. Use the smallest
  useful subset rather than running a ceremonial full workshop.
- [SEI Attribute-Driven Design](https://www.sei.cmu.edu/library/attribute-driven-design-method-collection/)
  — recursively decompose from architecture-significant requirements when the design is
  large enough to need a staged method.
- [Architecture Decision Records community](https://adr.github.io/) and
  [MADR](https://adr.github.io/madr/)
  — concise, versioned decision records with status and supersession.
- [Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
  and [Fowler's ADR explanation](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
  — rationale should survive the implementation and its authors.
- [Building Evolutionary Architectures](https://nealford.com/books/buildingevolutionaryarchitectures.html)
  and [architectural fitness functions](https://www.thoughtworks.com/en-us/radar/techniques/architectural-fitness-function)
  — turn important architectural properties into executable or observable checks.

## Scenario branches

Read a branch only when its driver is present.

### Data, distribution, and reliability

- [Designing Data-Intensive Applications](https://martin.kleppmann.com/2017/03/27/designing-data-intensive-applications.html)
  — replication, partitioning, transactions, consistency, streams, and data evolution.
  Record the edition and access date when using the changing second edition.
- [Distributed Systems](https://www.distributed-systems.net/) by van Steen and Tanenbaum
  — broader system models and failure assumptions.
- [Paxos Made Simple](https://www.microsoft.com/en-us/research/publication/paxos-made-simple/)
  and [Raft](https://raft.github.io/) — load only for an actual consensus or replicated-log
  problem.
- [Jepsen](https://jepsen.io/) — failure injection and consistency testing. Treat a
  product report as evidence about that product, not a universal theorem.
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
  — shared names for idempotency, retries, dead letters, correlation, routing, and
  backpressure.
- [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/)
  — failure propagation, timeouts, circuit breakers, bulkheads, and recovery.
- [Google SRE books](https://sre.google/books/) — SLOs, error budgets, capacity, and
  release reliability. Translate “reliable” into an observable target.

When using CAP, PACELC, FLP, or clock/order models, state the failure model, read/write
semantics, consistency level, and meaning of availability. A slogan is not a scenario.

### Data and interface evolution

- [Evolutionary Database Design](https://martinfowler.com/articles/evodb.html) — additive
  changes, compatibility windows, backfills, dual-read/write transitions, and rollback.
- Official [OpenAPI](https://spec.openapis.org/oas/latest.html),
  [AsyncAPI](https://www.asyncapi.com/docs), protocol-buffer, Avro, or schema-registry
  documentation — use the version that the repository actually targets and record the
  compatibility policy.
- CQRS, event sourcing, data mesh, microservices, and serverless are conditional options.
  Load their material only when a driver such as auditability, team ownership, or read/write
  asymmetry makes the option relevant.

### Performance and feasibility

- [USE Method](https://www.brendangregg.com/usemethod.html) and
  [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html)
  — investigate utilization, saturation, and errors before changing structure.
- [Little's Law](https://pubsonline.informs.org/doi/10.1287/opre.1110.0940) — relate
  throughput, concurrency, and latency assumptions; use it as a model, not a fake precise
  forecast.
- [Gil Tene on latency measurement](https://www.infoq.com/presentations/latency-response-time/)
  — histograms, percentiles, warm-up, and coordinated omission.
- [TLA+ / Specifying Systems](https://www.microsoft.com/en-us/research/publication/specifying-systems-the-tla-language-and-tools-for-hardware-and-software-engineers/),
  [Alloy](https://alloytools.org/), and property-based testing — use for a concrete
  concurrent state machine, protocol, permission model, or invariant whose failure cost
  justifies the work.

### Legacy, evolution, and socio-technical boundaries

- [Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
  — seams, isolation, and characterization tests.
- [Software Aging](https://dl.acm.org/doi/10.1145/257734.257788) — a reminder to make
  design recovery and drift checks recurring work, not a one-time rewrite.
- Strangler Fig, Branch by Abstraction, and Continuous Delivery are migration techniques;
  require a compatibility window, rollback, and sensor before selecting one.
- [Conway, How Do Committees Invent?](https://www.melconway.com/research/committees.html)
  — inspect communication and ownership boundaries without mechanically copying team
  structure into directories.
- [Team Topologies](https://teamtopologies.com/) — load for service ownership and team
  interaction decisions; verify the edition and treat it as guidance.
- [DORA research](https://dora.dev/research/) — use current delivery and reliability
  measures when an organizational or platform change is part of the architecture.

## Coding-agent and harness material (time-sensitive)

These are practice reports, not standards. Record their publication date and verify that
the mechanism still applies to the host agent.

- [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
  (Fowler and Böckeler, 2026-04) — feedforward guides, feedback sensors, computational
  versus inferential feedback, quality-left, and architecture fitness harnesses.
- [Maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html)
  (Böckeler, 2026-05) — dependency and coupling rules, structural review, mutation
  testing, and feedback that an agent can act on. Do not copy its thresholds blindly.
- [OpenAI Harness engineering](https://openai.com/index/harness-engineering/)
  (2026-02) — one team's use of hierarchy, structural tests, custom linters, observability,
  and a repository knowledge map. Extract mechanisms; do not generalize the architecture.
- [Anthropic effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  and [harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)
  — initializer, progress artifacts, handoff, and planner/generator/evaluator separation.
- [Stripe Minions](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
  — isolated environments and bounded feedback loops. Treat platform details as local
  practice, not a portable requirement.
- [Codex internet access](https://developers.openai.com/codex/cloud/internet-access)
  and [agent configuration](https://developers.openai.com/codex/agent-configuration/agents-md)
  — current host behavior; re-check before relying on it.

## Supply-chain and dependency signals

Use [OpenSSF Scorecard](https://scorecard.dev/), [OSV](https://osv.dev/),
[SLSA](https://slsa.dev/), [Dependabot](https://docs.github.com/code-security/concepts/supply-chain-security/dependabot-version-updates),
or [Renovate](https://docs.renovatebot.com/upgrade-best-practices/) to find signals. They
support, but do not replace, compatibility and semantic review. [Thoughtworks Technology
Radar](https://www.thoughtworks.com/en-us/radar) and the [CNCF Landscape](https://landscape.cncf.io/)
are discovery indexes, not approval gates.
