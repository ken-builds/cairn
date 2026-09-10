---
name: implementation-rationale
description: Public contracts and implementation rationale. Use while changing exported declarations, failure handling, lifecycle or compatibility behavior, and when auditing their source documentation against the final implementation.
---

# Implementation Rationale

Preserve consumer contracts and non-obvious implementation reasons while code changes.
Use the narrowest applicable branch; ordinary private edits with no contract/rationale
change need no ledger or record. This skill owns source documentation and its evidence,
not a full API guide or general code review.

## Scope and authority

In `implementation` mode, maintain findings during the authorized change. In `audit` mode,
inspect an existing diff/surface and return dispositions. Reuse the user's authorization
for in-scope code and documentation; discovery alone does not expand write scope.
Architecture decisions follow the repository's decision process.

Evidence states are `confirmed`, `inferred`, `unknown`, `not-run`, and `blocked`. An explicit
record of a failed check is evidence, not a passing result. The **ledger** accounts for
discovered findings; **placement** is each finding's primary source of truth.

## 1. Inventory the changed surface

Read applicable repository instructions, source documentation conventions, existing decisions,
exports/entrypoints, and generated API configuration. Capture revision, protected changes,
and the final or current diff. Use declarations, consumers, and configuration to identify
changed public symbols, members, and affected call/implementation sites. For an explicit
whole-API audit, inventory that scope rather than only the diff.

Read [public-api-comments.md](references/public-api-comments.md) when exported declarations
change. Distinguish public, internal, closed vocabularies, and open-ended values. Record
the inventory source and its coverage gaps; a name alone does not establish a contract.

**Done when:** every public item discovered in the scoped declarations/exports has an
existing contract, a coverage finding, or a reason it is internal. Generated surface
differences and unavailable declaration/consumer evidence remain visible.

## 2. Inspect reasons at the change boundary

On failure handling, lifecycle, or compatibility changes, read
[failure-semantics.md](references/failure-semantics.md) before choosing guards or recovery.
Check the affected producers, consumers, and implementations against the promised behavior.
On a non-obvious ordering, ownership, or simplification decision, read
[comment-placement.md](references/comment-placement.md) to select where the reason belongs.

For each finding, capture the observation, source, impact if changed, likely wrong
simplification, and disposition. Search for evidence that contradicts a comment or assumed
invariant; resolve a mismatch before documenting it as an intended guarantee.

**Done when:** each changed failure/lifecycle path found in the scoped diff has an explicit
outcome and recovery owner or open question; each discovered contract/rationale mismatch
has a disposition. Documented reasons describe the verified behavior, not an imagined fix.

## 3. Place knowledge and maintain the checkpoint

Place the finding where its reader needs it:

- Consumer meaning belongs at the public declaration or canonical API reference.
- A local invariant or non-obvious choice belongs beside the code that relies on it.
- Observable behavior belongs in a regression test or repository-native sensor.
- Multi-file implementation discoveries belong in an Implementation Record when needed.
- A changed architecture decision belongs in its authoritative Brief/ADR process.
- Versions, commands, and generated facts remain in their environment source of truth.

Keep one authoritative explanation and link secondary locations. Use native public API
documentation for symbol/member contracts. For maintainer comments, state the protected
property and why an otherwise plausible change would violate it. Routine code closes with
no comment when its structure already communicates the reason.

At each implementation increment, update existing notes/ledger with changed boundaries,
contracts, invalidated assumptions, and checks. Before adding/splitting components or
changing public entrypoints/allowed edges, use `repository-structure` if installed;
otherwise inspect those relations directly and retain any uncovered checks. For a changed
cross-module design, use the installed architecture skill or expose the pending decision.

**Done when:** each finding has one primary placement or an owned open question. The
checkpoint matches the current change; documentation volume is not a completion measure.

## 4. Record only what needs durable context

Read [implementation-record-contract.md](references/implementation-record-contract.md) when
findings span placements, a material failure/compatibility/migration issue needs context
beyond code and tests, or the user requires a handoff. Follow existing record conventions;
otherwise use `docs/implementation/records/<slug>.md`. Preserve completed records as history.
A finding fully preserved by code and its sensor closes as `record not warranted`.

**Done when:** a record, when warranted, accounts for the discovered finding IDs and links
their placements, rejected approaches, and unresolved checks. Reuse existing records rather
than adding documents for every checkpoint or copying public API descriptions into tables.

## 5. Verify the final contract and coverage

Reconcile the final diff, declarations, tests, comments, and relevant decisions. Compare
the scoped public inventory with its documented surface and inspect generated output when
published. Add the cheapest applicable check for each relied-on changed contract.

For each executed check, record targets actually selected and pass/fail/skip outcomes.
For a new/materially changed critical gate, demonstrate failure on a controlled violation
and a pass on its valid counterpart in isolation, or leave effectiveness `unknown`.
Run `scripts/validate_implementation_record.py` when a record exists; it checks record
structure/links, not API coverage or runtime truth. Run relevant native checks, and confirm
the owning gate actually selects the intended surface rather than silently skipping it.

**Done when:** every discovered public item and changed contract has a verified disposition
or explicit gap; drift has a decision or next action. Keep document validity, check coverage,
and behavioral results distinct. An unrun or skipped check cannot close its contract.

Finish with changes, actual verification scope, record links or `record not warranted`,
and remaining decisions. Source, tests, and records own the detail.
