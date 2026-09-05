# Public API comments

Use this reference when a change exposes or audits a source-level public API. The goal is a
discoverable, current contract for consumers, not a complete user manual and not an implementation
history.

## Surface classes

Classify declarations before writing:

- **Exported symbol** - a function, class, interface, type alias, constant, module, or public field
  reachable through the supported entrypoint.
- **Structured member** - a field, method, parameter, result member, or lifecycle member exposed by
  an exported type or class.
- **Closed vocabulary** - a finite set of public cases such as an enum, literal union,
  discriminant, error/status/event code, hook name, or exported finite constant list.
- **Open value** - a string, number, or extension point whose valid future values are not listed in
  the source. Document its format, constraints, and extension policy instead of inventing member
  coverage.
- **Internal** - intentionally unreachable from the supported public entrypoint. It needs no API
  comment unless a rationale, security boundary, or accidental exposure requires one.

Do not confuse a descriptive name with a complete contract. `CONFLICT`, `State`, or `create()` may
still need the boundary, lifecycle, failure, or caller-action semantics that the name omits.

## Coverage levels

Use the smallest level that makes the public contract unambiguous:

1. Every intended exported symbol gets a concise summary.
2. Every member of a public structured type gets a concise role and constraint description. Every
   member of a public closed vocabulary gets a member-level meaning or a unique canonical entry.
3. Document parameters, returns, errors, side effects, lifecycle, stability, deprecation, and
   compatibility when they affect how a consumer calls or evolves the API.

For machine-readable codes and tags, a useful member description answers, as applicable:

- what condition produces or accepts the member;
- which boundary or operation owns it;
- what the caller should do next, including retry or terminal behavior;
- whether it is stable, deprecated, reserved, or version-specific; and
- which related event, state, or result it describes.

Derive these claims from call sites, tests, architecture records, and authoritative specifications.
Do not promote an inference to a public guarantee merely because a name suggests it.

## Placement and format

Put the short contract where consumers discover the declaration, using the repository's native
format: TSDoc/JSDoc, Rustdoc, kernel-doc, Go documentation comments, or the local equivalent.
Use parameter, return, throws, deprecation, and see-also tags only when the local toolchain supports
and benefits from them. A generated API reference may hold a larger matrix, but the source remains
the canonical location unless the repository explicitly chooses another source.

The Linux Kernel analogy is about two decisions, not C syntax. General commenting guidance keeps
mechanical `HOW` in the code and reserves comments for meaningful behavior; kernel-doc structures
public functions and types, including enumeration members, so generated documentation has complete
consumer coverage. Adapt both principles to the host language and its documentation tooling.

For a TypeScript literal union, member-level comments are a valid first choice:

```ts
/** Stable machine-readable failures returned by the public API. */
export type ErrorCode =
  /** The request cannot be applied to the current revision. */
  | "CONFLICT"
  /** The resource has reached its terminal lifecycle boundary. */
  | "DISPOSED";
```

Verify that the project's declaration or API documentation generator retains comments attached to
union members. If it does not, use one canonical member catalog in the same source file or a linked
API reference; do not maintain two independently edited descriptions.

## Audit procedure

1. Read supported entrypoints and generated declarations to enumerate the intended surface.
2. Search each symbol and member across implementation, tests, records, and docs to recover actual
   conditions and compatibility semantics.
3. Mark each item `documented`, `stale`, `missing`, `internal`, or `open-ended` in the coverage
   ledger. Explain an intentional exclusion.
4. Write or repair the source comments, then inspect generated output and run the repository's
   native documentation, type, and contract checks.
5. Recheck additions and removals as a compatibility event. A new public case needs documentation
   in the same change; a removed or renamed case needs a deprecation or migration decision when the
   API is already consumed.

## No-op and boundary tests

Leave out a comment that only repeats a symbol name, a type keyword, a loop, or an obvious literal
from private implementation code. For a public member, a deliberate repository convention may
choose a shorter description when the signature is genuinely complete, but that choice must be
visible in the coverage audit rather than treated as an undocumented omission.
Keep historical alternatives, probe results, and implementation reasons in an Implementation
Record or ADR. Keep volatile package versions and generated command details in the manifest,
lockfile, or build system. Public API coverage and implementation rationale may link to those
sources but should not duplicate them.

Public documentation is complete only when every intended exported symbol has a contract summary,
every public closed-vocabulary member has coverage, open values have an extension rule, generated
output has been checked when it is published, and no comment contradicts the implementation or its
authoritative decision record.
