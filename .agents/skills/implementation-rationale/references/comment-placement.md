# Comment placement

This reference separates two comment layers. Use public API comments to state the contract a
consumer discovers at an exported declaration. Use rationale comments to preserve a non-obvious
reason a maintainer could accidentally remove or change. Neither layer is a transcript of the
implementation.

## First route the layer

Ask which reader needs the information:

- **Consumer** - place a concise API documentation comment at the exported symbol or member. Read
  [public-api-comments.md](public-api-comments.md) for coverage and contract detail.
- **Maintainer** - place a rationale comment beside the smallest code boundary whose simplification
  would violate an invariant, ordering rule, compatibility promise, trust boundary, or failure
  guarantee.
- **History or decision owner** - place implementation history in an Implementation Record and a
  durable cross-module choice in an ADR. Keep the source comment as a link, not a duplicate.

Do not use a rationale comment to compensate for a missing public API description, or use an API
comment to hide a changed architecture decision.

## Rationale decision test

For a maintainer-facing comment, ask three questions in order:

1. Would a competent maintainer likely make a wrong change from the code and signature alone?
2. Would that change violate a contract, invariant, security boundary, failure guarantee, or
   compatibility promise?
3. Can the reason be stated locally and linked to one authoritative record or specification?

Write a rationale comment when all three answers are yes. A no-op comment answers only "what this
line says" or repeats a name; leave it out and improve the code or sensor instead.

## Placement matrix

| Finding | Primary placement | Comment shape | Sensor or record |
| --- | --- | --- | --- |
| Exported function, class, interface, or type alias | Public declaration | Concise consumer-facing summary and applicable contract details. | Native API-doc output or declaration check. |
| Member of an exported structured type | Public member declaration | State the member's role, constraints, and lifecycle. | Contract test; public API coverage. |
| Member of a public closed vocabulary | Member declaration or one canonical member catalog | Define the case and caller/emitter semantics; cover every member. | API-doc output or coverage audit. |
| Invariant that a refactor could violate | Function or data declaration | State the invariant and why it is enforced here. | Focused test; link ADR/record when present. |
| Non-obvious ordering or commit boundary | Boundary function or short block | State the observable failure if the order changes. | Failure or concurrency test; Implementation Record. |
| Library or protocol behavior differs from intuition | Adapter boundary | Name the observed behavior and supported profile. | Negative compatibility fixture; versioned record. |
| Trust, parsing, or resource limit | Validation boundary | State what is untrusted and why the guard precedes the next call. | Security or malformed-input test; specification link. |
| Crash window, retry, or idempotency rule | Lifecycle/transaction boundary | State the recovery consequence and required caller behavior. | Fault-injection test; Implementation Record/ADR. |
| Implementation history or rejected alternative | No source comment by default | Keep the local code concise. | Implementation Record or ADR. |

## Rationale writing shape

Prefer two short sentences:

```text
// Preserve <ordering/guard> because <invariant or failure consequence>.
// See <repository-relative record or specification>.
```

Use the exact local comment syntax and language. Omit the second line when the reason is stable,
self-contained, and no useful source exists. Link a specific heading or finding ID when the
repository supports stable anchors. Keep links relative for repository material and use an
authoritative external specification for a protocol or library contract.

The Linux Kernel's [commenting guidance](https://docs.kernel.org/process/coding-style.html#commenting)
is a useful bar: make the working obvious in code, avoid explaining mechanical `HOW`, and reserve
small comments for something especially clever, awkward, or consequential. Adapt that principle to
the host language; do not copy C formatting or require a comment count.

## Placement review

Before closing a finding, check:

- the selected layer matches the reader who needs the information;
- the comment sits beside the declaration or code whose change would invalidate it;
- its nouns match the repository Glossary and current API;
- its claim is supported by a test, record, ADR, or specification;
- it does not freeze a volatile version, line number, or temporary workaround without an owner;
- it does not describe a deferred feature as current behavior; and
- deleting it would make a future mistake more likely for the intended reader.

When the last check is false, record `comment not warranted` in the ledger and keep the knowledge
in the more appropriate source.
