---
name: greenfield-foundation
description: Initial system boundaries. Use when a new system or disposable prototype needs its first architecture, repository layout, or end-to-end implementation slice before stable contracts exist.
---

# Greenfield Foundation

Select the smallest defensible foundation and an executable first slice. Production consumers,
persistent data commitments, or stable modules make their evolution an `architecture-design`
task when that skill is installed. In a mixed project, separate new foundation choices from
changes to relied-on boundaries. Framework or directory names are proposals, not evidence.

## Scope and authority

Reuse authorization already given: `design` permits read-only investigation, `probe` permits
bounded isolated experiments, and `record` permits Brief/ADR writes. Product implementation
and provisioning require their own authorized scope; this workflow specifies their handoff.
Ask only when the next operation exceeds the existing scope, not on each named phase.

Discover record conventions; otherwise use `docs/architecture/briefs/` and
`docs/architecture/decisions/`. A read-only design may stay in the response. Evidence uses
`confirmed`, `inferred`, `unknown`, `not-run`, and `blocked`; record a failed hypothesis as
such even when the experiment ran successfully.

## 1. Establish the mandate and search boundary

Inspect supplied requirements, examples, existing prototypes, environment constraints, and
local instructions. Capture protected state, intended users/outcomes, non-goals, ownership,
delivery and operating constraints. Trace relevant user journeys through external systems,
data owners, trust boundaries, and lifecycle transitions to create the target **Map**.

For each boundary found in these inputs, state its purpose, contracts, hidden decisions,
consumers, and evidence or uncertainty. Record consulted sources and unavailable inputs.

**Done when:** each journey/boundary discovered in the scoped inputs is mapped or has a
next check, and each proposed responsibility is tied to an outcome. Missing product intent
that would change the foundation is an open decision, not a silently chosen requirement.

## 2. Discriminate the assumptions and candidates

Define introduced, overloaded, or cross-boundary domain terms in the **Glossary**, reusing
existing definitions. Convert goals into finite **drivers** with observable acceptance
conditions; use numeric thresholds for quantitative properties and rank conflicting drivers.

Read [decision-lenses.md](references/decision-lenses.md) when choosing style, ownership,
integration, data, build-versus-buy, or operating boundaries. Start **C0** with the smallest
reversible foundation and add materially different options when a driver warrants them.
For each discovered premise that can change the choice, use the claim-discovery branch of
[evidence-and-probes.md](references/evidence-and-probes.md): identify counterevidence and the
decision it would change before selecting a source lookup or isolated probe.

**Done when:** candidates are compared on relevant drivers, new abstractions name their
consumers and hidden variation, and each decision-changing premise has evidence, a next
check, or an explicitly accepted risk. More candidates or questions are not a quota.

## 3. Specify boundaries and the first slice

Specify only the selected foundation's required contracts: responsibilities, dependency
direction, API/data ownership, validation and failure semantics, lifecycle, trust boundaries,
and relevant runtime/deployment/operating constraints. Tie each choice to a driver and
revisit trigger. Keep unsupported service-level or capacity promises as assumptions.

Before proposing new component paths, public entrypoints, or allowed dependency edges,
use `repository-structure` when installed. If unavailable, identify contract and implementation
ownership, visible entrypoints, hidden details, and expected substitution impact in the Map;
choose physical grouping from those relations rather than a fixed directory template.

Read [bootstrap-gates.md](references/bootstrap-gates.md) when defining the first end-to-end
slice and its ordered gates. Describe acceptance across real boundaries, rollback, and checks
that future implementation must pass. Unbuilt slices remain planned rather than validated.

**Done when:** an implementer can identify the first slice's boundaries, observable outcome,
pending assumptions, and dependencies without inventing a cross-cutting contract. Deferred
features have an explicit scope boundary; deployment and provider choices remain conditional.

## 4. Record and hand off

Before writing a Foundation Brief or ADR, read
[foundation-contract.md](references/foundation-contract.md). Reuse existing Map/Glossary
sources; keep each durable rationale in its ADR. Run `scripts/validate_foundation.py` for
record structure and report its scope separately from architectural/behavioral validation.

Hand off a short checkpoint in existing notes or the Brief: selected boundaries, contracts
to preserve, unresolved assumptions, and checks for the next increment. On public declaration
changes, the implementer uses `implementation-rationale`'s public-contract branch; on
failure/lifecycle/compatibility changes, its rationale branch. Apply during implementation,
then reconcile the final diff. If unavailable, preserve consumer contracts and non-obvious
reasons at their owning code/tests and list pending coverage.

**Done when:** the chosen foundation, rejected alternatives, first increment, evidence
limitations, and next authorized work are explicit. Record acceptance does not mark future
implementation or deployment checks as passed.

## 5. Define verification and revisit triggers

For each contract the first slice relies on, specify a repository-native check or operational
observation and an owner. When implementation runs it, capture selected targets and actual
pass/fail/skip outcomes. A new/materially changed critical gate needs an isolated valid fixture
and controlled violation proving detection, or effectiveness `unknown` with a next check.

At the next increment, compare new boundaries, changed contracts, and invalidated assumptions
with the checkpoint. Reopen the relevant choice and update its checks. Once contracts are
relied upon, route their subsequent evolution through `architecture-design` when available.

**Done when:** each relied-on contract has an applicable result or pending check, and coverage
gaps are visible. Keep record validity, sensor coverage, and observed behavior separate.

Finish with the foundation choice, trade-offs, record links, first slice, actual verification
scope, and open decisions. Keep detailed contracts in their authoritative records.
