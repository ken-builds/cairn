---
name: architecture-design
description: Architecture changes in an existing system. Use before changing cross-module contracts, dependency choices, data or runtime boundaries, or recovery behavior; revisit when implementation invalidates a design assumption.
---

# Architecture Design

Produce an evidence-backed decision for an existing system. Start from its actual contracts
and the requested change. A local edit that preserves those contracts needs local verification,
not a full investigation. For a new system without relied-on boundaries, use
`greenfield-foundation` when installed, or identify the missing foundation.

## Scope and authority

Carry forward the user's authorized scope: `design` permits read-only investigation;
`probe` permits bounded isolated experiments; `record` permits durable documentation.
Implementation requires implementation scope. These labels describe permitted operations,
not a sequence of approval requests. Reuse existing authorization; ask only for an operation
outside it. Keep another project's working checkout outside experiments.

Use the repository's record conventions. With no convention, place Briefs in
`docs/architecture/briefs/` and durable decisions in `docs/architecture/decisions/`.
A read-only review may remain in the response. Distinguish evidence states `confirmed`,
`inferred`, `unknown`, `not-run`, and `blocked`; a confirmed observation can reject a claim.

## 1. Bound the investigation

Read applicable agent/contribution rules, manifests, build/test entrypoints, configuration,
and existing decisions. Capture the baseline revision and protected changes. State the
outcome, non-goals, affected environments, and current authorization.

Trace the requested flow from entrypoints through callers, exports, configured wiring,
state owners, and external effects. Build the **Map** from these discovered boundaries,
with a source for each edge. Expand when a newly found edge affects the requested behavior;
record unavailable graph/configuration information and where tracing stopped.

**Done when:** every boundary found by the recorded searches has a responsibility, relevant
consumer/producer, contract, and source or next check. Search scope and unresolved edges
are visible; this accounts for discovered objects rather than claiming to know every risk.

## 2. Test the premises

Reconcile domain terms introduced, renamed, overloaded, or used across affected boundaries
in the **Glossary**. Cite existing definitions and identify aliases or semantic conflicts.
Turn requirements into finite **drivers** with observable acceptance conditions; use numeric
thresholds for quantitative properties and identify conflicting priorities.

Read [design-judgment.md](references/design-judgment.md) when an assumption could change the
choice, a new abstraction is proposed, or failure/lifecycle behavior changes. Follow the
applicable branch to seek counterevidence; treat an unverified premise as a question rather
than an extra runtime state. Read [reading-map.md](references/reading-map.md) when a particular
architecture lens or external precedent would help resolve that question.

**Done when:** changed/cross-boundary terms have definitions, each driver has an acceptance
condition, and each discovered decision-changing premise has evidence or an explicit next
check and impact if false. Ask for missing user intent only when it changes the choice.

## 3. Compare and discriminate

Keep **C0** as the current design or smallest safe change. Add materially different candidates
where a driver or uncertainty warrants comparison. Compare ownership, information hiding,
dependency direction, complexity, failure propagation, operations, compatibility, and rollback
only as they affect the drivers. State what would change the preferred candidate.

- For version-sensitive library, protocol, security, or compatibility claims, read
  [evidence-research.md](references/evidence-research.md), verify primary sources against the
  actual environment, and retain the claim's source/version/date.
- For an unresolved premise that could reorder candidates, read
  [probe-and-benchmark.md](references/probe-and-benchmark.md). Define the hypothesis,
  discriminating outcome, budget, and isolation before the smallest useful experiment.
- Before adding/splitting a component, moving a public entrypoint, or changing allowed
  dependencies, use `repository-structure` when installed. Pass the Map and drivers;
  reuse its findings. If unavailable, assess paths, visibility, and allowed edges here
  and identify checks that remain uncovered.

**Done when:** each selected trade-off connects to a driver and sourced fact, measurement,
or labeled inference. Each material unknown has a next check, accepted risk, or blocked
decision. Probe results include failure and skipped work, not just successes.

## 4. Record the decision and implementation checkpoint

Before writing records, read [artifact-contract.md](references/artifact-contract.md).
Record the selected candidate, rejected alternatives, evidence, and revisit triggers.
Keep rationale authoritative in one ADR; link existing Map/Glossary entries. Identify
migration/rollback effects and the first implementation checkpoint.

The checkpoint names selected boundary changes, contracts to preserve, assumptions still
open, and checks needed for this increment. Reuse task notes or the existing record;
a checkpoint does not require a new document. When authorized implementation begins:

- On public declaration changes, use the public-contract branch of `implementation-rationale`.
- On failure handling, lifecycle, or compatibility changes, use its rationale branch.
- Apply these branches during the change and reconcile the final diff. If that skill is
  unavailable, preserve changed consumer contracts and non-obvious reasons beside their
  owning code/tests, and list unresolved coverage in the handoff.

**Done when:** the decision identifies exact boundaries, implementation scope, relevant
contracts, evidence limitations, and next checks without relying on conversation memory.
An unrun implementation check is still `not-run`, even when the design is accepted.

## 5. Verify coverage and reconcile drift

For contracts relied on by this increment, identify the cheapest applicable **sensor**:
dependency/visibility rule, API/schema check, behavior test, compatibility fixture, benchmark,
or operational signal. Record actual targets selected and outcomes, including skips.
For a new or materially changed critical gate, demonstrate detection of a controlled
violation in an isolated fixture and a pass on the valid counterpart, or leave its
effectiveness `unknown` with a next action. Preserve a fixture when it guards a real risk.

Compare the final diff and discovered edges with the checkpoint. New boundaries, failed
assumptions, or changed contracts reopen the relevant step; supersede the decision when
intent changes. If implementation is outside this task, hand off these checks as pending.

**Done when:** every checkpoint contract has an applicable result or named coverage gap;
record-format validity, gate coverage, and behavioral evidence are separate claims.
The Map reflects the inspected revision/diff and the handoff names remaining uncertainty.

Finish with the decision, key trade-offs, record links, actual verification scope, and next
action. Scale the response to the change; records own the detailed reasoning.
