---
name: implementation-rationale
description: Maintain source-level public API documentation and implementation rationale during code changes, covering exported symbols, members, parameters, errors, invariants, ordering, compatibility traps, failure semantics, security boundaries, and design drift.
---

# Implementation Rationale

Use this skill during or immediately after implementation when public source documentation or
non-obvious implementation knowledge could be lost while code is simplified, moved, or reused.
It covers source-level public API documentation and maintainer rationale, plus their relationship
to tests, implementation records, and architecture decisions. It does not replace a full API
guide, README, release notes, ADR, or a generic code review.

The deliverable is a complete **ledger** of decision-relevant findings and a **placement** for
each one: a public API comment, an implementation rationale comment, an executable sensor, an
Implementation Record, an ADR/Brief update, an environment source of truth, or an explicit
decision that no durable note is warranted. The response is an index; the code, tests, and linked
records remain the sources of truth.

## Invocation and operating contract

This skill is model-invoked so an implementation agent can reach it when a documentation branch
appears; it is also available as `$implementation-rationale` for an explicit audit. Automatic
discovery does not grant permission to mutate a repository. A review or a task without write scope
returns a disposition plan. A task that authorizes implementation and its documentation may apply
the placements in scope; architecture-record changes still follow the repository's own gate.

Choose the narrowest mode:

- **implementation** - capture and place documentation findings while code is being built or
  changed.
- **audit** - reconstruct the public API surface and implementation findings from an existing
  diff, declarations, tests, commands, and records, then identify missing, stale, duplicated, or
  misplaced documentation.

Read [public-api-comments.md](references/public-api-comments.md) when an exported API surface,
member contract, or generated API document is involved. Read
[comment-placement.md](references/comment-placement.md) when choosing maintainer rationale or
deciding that a comment is a no-op. Read
[implementation-record-contract.md](references/implementation-record-contract.md) before
creating or validating an Implementation Record. Run
`scripts/validate_implementation_record.py` whenever a record is present.

## Stable vocabulary and two layers

Keep these leading words stable:

- **surface** - the declarations and members intentionally exposed to consumers.
- **contract** - the behavior a consumer may rely on, including errors, lifecycle, and stability.
- **coverage** - an explicit documentation disposition for every required public surface item.
- **finding** - an observed implementation fact, mismatch, or discovery with an impact.
- **rationale** - the reason a future edit must preserve a choice or constraint.
- **ledger** - the exhaustive accounting of findings and their destinations.
- **placement** - the chosen primary source of truth for a finding.
- **record** - the durable, implementation-specific account of what happened and why.
- **drift** - a difference between implementation and an accepted design or contract.
- **sensor** - an executable or observable check that detects regression of the contract or rationale.

The two documentation layers are deliberately separate:

- **Public API documentation** is consumer-facing. Every intended exported symbol gets a concise
  contract summary. Every member of a public structured type and every member of a public closed
  vocabulary gets a member-level meaning or a unique canonical documentation entry. Parameters,
  returns, errors, side effects, lifecycle, stability, and deprecation are documented when they
  are part of the usable contract.
- **Implementation rationale** is maintainer-facing. It explains non-obvious invariants, ordering,
  compatibility traps, trust boundaries, failure windows, concurrency, and deliberate trade-offs.
  Private or local values need this layer only when the code and signature do not protect the
  reason by themselves.

## Workflow

### 1. Establish the baseline

1. Read repository-local instructions, manifests and lockfiles, build/test commands, source
   comment conventions, API documentation tooling, exports, and documentation layout. Locate
   relevant Briefs, ADRs, Probes, previous Implementation Records, and task authorization.
2. Capture the branch, `HEAD`, index/worktree status, untracked paths, protected changes, and the
   implementation scope. Inspect the complete diff, generated declarations or docs, changed tests,
   and commands or probes that shaped the change.
3. Separate repository facts, observed implementation results, contract claims, and assumptions.

**Done when:** every changed boundary and available contract input has an identified source, the
protected baseline is recorded, and the write scope is explicit.

### 2. Map the public surface

Read [public-api-comments.md](references/public-api-comments.md).

1. Trace package entrypoints, exports, public headers, generated declarations, and documented
   symbols. Classify each item as public, internal, or open-ended. Identify closed vocabularies:
   enums, literal unions, discriminants, error/status/event codes, hook names, and finite constants.
2. Record existing symbol-level and member-level documentation, including generated output. Mark
   an undocumented or stale item as a coverage finding; do not infer that a descriptive name is a
   complete contract.
3. Keep private implementation details out of the public inventory unless they are accidentally
   exposed or affect a public guarantee.

**Done when:** the intended public surface, closed vocabularies, documentation locations, and
coverage gaps are visible; open values are not mistaken for finite member lists.

### 3. Build the finding ledger

1. Read the diff, tests, declarations, and records for behavior that would be easy to remove,
   reorder, broaden, or misunderstand. Include public contract gaps alongside implementation
   invariants, compatibility traps, trust boundaries, failure windows, concurrency, and lifecycle
   semantics.
2. Give each finding a stable ID. Record the observation, evidence location or command, impact if
   changed, likely wrong simplification, intended layer, and state. Capture findings when they
   become stable enough to affect a contract or code; reconcile them at each implementation
   checkpoint.
3. Mark ordinary naming, obvious control flow, generated detail, volatile lookup data, and
   speculation as routine or open work rather than manufacturing a comment.

**Done when:** every decision-relevant behavior and every public coverage gap has one ledger entry,
and every plausibly affected region has either a finding or an explicit routine disposition.

### 4. Choose the placement

For every finding, choose one primary source of truth:

- a public symbol or member contract belongs in the language-native API documentation comment or
  the repository's canonical API reference;
- a local invariant, ordering rule, compatibility trap, or trust boundary belongs beside the code
  that would be incorrectly changed;
- a behavior that must not regress belongs in a test or another executable sensor;
- a multi-file discovery, measured result, rejected approach, or residual risk belongs in an
  Implementation Record;
- a cross-module or long-lived architecture choice belongs in the authoritative ADR or Brief;
- dependency versions, commands, and generated artifact facts stay in their environment source of
  truth;
- an unresolved concern becomes an owned open question with a next check.

Link instead of copying the same meaning into several artifacts. If a finding changes public
behavior or an accepted decision, route it through drift reconciliation before polishing comments.

**Done when:** every ledger entry has one primary source of truth, secondary links are named, and
no rationale or contract is split across competing authoritative locations.

### 5. Write public API documentation

Read [public-api-comments.md](references/public-api-comments.md) when this branch is present.

1. Use the repository's native documentation format. Give each intended exported symbol a concise
   summary. Document every member of public structured types and every member of a public closed
   vocabulary; include accepted/emitted conditions, caller action, error or retry semantics,
   lifecycle, side effects, stability, and deprecation when applicable.
2. Put the documentation at the declaration or member boundary that consumers discover. Keep the
   source comment concise and move a large matrix or history to the canonical API reference or
   Implementation Record.
3. Inspect generated declarations or API output when the project publishes them. If the tool does
   not retain member comments, choose one canonical source representation and record the limitation
   rather than maintaining conflicting copies.

**Done when:** every intended public symbol has contract coverage, every public closed-vocabulary
member has a semantic description or unique canonical entry, and generated output does not silently
drop required documentation.

### 6. Write implementation rationale

Read [comment-placement.md](references/comment-placement.md).

1. Put rationale at the smallest stable boundary whose simplification would violate the finding,
   usually a function or data declaration and only occasionally a narrow internal block.
2. State the protected invariant or observable consequence and why the choice is non-obvious. Let
   the implementation carry the mechanical explanation; link a local ADR, record, probe, or
   authoritative specification when useful.
3. Keep public API contract text and maintainer rationale distinct. Do not use an implementation
   comment to hide a missing public API description or a changed architecture decision.

**Done when:** each rationale comment is adjacent to the protected code, states a reason a future
edit could violate, and adds no unsupported behavior or historical diary.

### 7. Create or update the Implementation Record

Read [implementation-record-contract.md](references/implementation-record-contract.md).

1. Follow the repository's established record location. When none exists, use
   `docs/implementation/records/<slug>.md`; do not move historical records solely to normalize
   layout.
2. Create a record when findings span multiple placements, a material compatibility/failure/
   security/migration/drift finding needs context beyond code and a sensor, or the user or
   repository requires an implementation handoff. A finding fully preserved by code and its sensor
   closes as `record not warranted`.
3. Include public-surface coverage only when that branch fired. Record the inventory and checks
   without duplicating every API description. Preserve rejected approaches, failed checks, crash
   windows, and unrun work when they affect future maintenance.
4. Update a draft at checkpoints. Preserve a completed record as history; later implementation
   work gets a new linked record.

**Done when:** the record accounts for every ledger ID, links each placement, distinguishes facts
from inference, and lets a fresh implementer understand the non-obvious shape without reopening the
conversation.

### 8. Reconcile drift and encode sensors

1. Compare implementation and generated API output with the Brief, ADRs, public schemas, declared
   exports, and non-goals. Classify each difference as routine implementation, confirmed refinement,
   accidental exposure, or contract/architecture drift requiring a new decision.
2. Add or update the cheapest sensor for each critical contract or rationale: API-doc generation,
   declaration inspection, focused test, schema check, type assertion, dependency rule, fault case,
   build/consumer check, or operational signal. Give an unrun sensor an owner and next action.
3. Keep comments, records, declarations, and tests aligned with final behavior. A comment that
   would become false after the next intended change is an open decision, not a completed placement.

**Done when:** every drift item has a decision, owner, or explicit deferral; public coverage is
complete; and every critical finding has a passing sensor or visible `not-run`/`blocked` follow-up.

### 9. Verify and hand off

1. Run the record validator when a record exists, then the repository's relevant format, lint,
   type, test, build, API-doc, and consumer checks. Check local links, source locations, generated
   artifacts, and the final diff.
2. Re-read public API comments as a consumer and rationale comments as a maintainer trying to
   simplify the code. Remove no-ops, strengthen ambiguous contract text, and update the ledger and
   record together.
3. Summarize the mode, surface coverage, record path or `record not warranted`, finding IDs and
   placements, verification states, unresolved boundaries, and next authorization.

**Done when:** the ledger is closed with no unassigned finding, public API coverage and rationale
comments pass their applicable audits, records pass structural checks, relevant sensors report
actual states, and the handoff contains links rather than a second copy of the contract.

## Boundary with neighboring skills

Use `architecture-design` or `greenfield-foundation` for the design model, evidence gate, probes,
and durable architecture decisions. Use `readme-authoring` for repository README content and
`git-commit-series` to organize the resulting diff. This skill owns source-level public API
documentation comments and implementation rationale discovered during implementation.

## Response handoff

End with a compact index: baseline and mode, public surface coverage, record link or `record not
warranted`, finding and placement counts, changed decisions, sensor/verification states, remaining
boundaries, and the next authorization. The code and records remain the long-lived source of truth.
