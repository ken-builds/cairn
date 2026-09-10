# Component design before paths

Use when adding/splitting components or changing dependency/visibility boundaries. Apply to
modules, packages, services, or plugins in the repository's native form. Keep findings in
the Structure Map and candidate comparison.

## Classify responsibility

For each affected group, identify its capability, owned state/invariants, reason to change,
entrypoints, and hidden mechanisms. Inspect actual references or native graphs; naming
resemblance alone does not establish cohesion. Distinguish contract, policy, implementation,
and composition where the change makes that distinction meaningful.

Keep an abstraction with the owner of its semantics. A contract about runtime behavior does
not automatically belong beside its runtime implementation. Identify who may construct
concrete implementations and which consumers depend only on their contract.

**Done when:** each proposed boundary explains what it owns and hides, with consumers and
evidence. Mixed responsibilities have a resolution or next check.

## Test substitution and grouping

Choose a plausible substitution or extension motivated by a current requirement. Name the
parts expected to change and consumer contracts expected to remain unchanged. Check whether
exposed types, configuration, or construction leak the replaced mechanism. Use a focused
consumer/contract test where it can verify this boundary.

Choose the smallest grouping that expresses the resulting ownership:

- Keep a homogeneous set of peers together even when numerous.
- Group by capability when it reduces cross-component coordination.
- Use local layers for stable dependency direction and information hiding.
- Introduce package/build/visibility units when enforceable independence earns their cost.

Interfaces, functions, schemas, protocols, and processes can express abstractions. A test
seam or trust boundary may justify one without multiple implementations. If current
consumers need no separation, retain concrete code and a revisit condition.

**Done when:** the grouping supports the substitution boundary and explains the expected
change footprint. Depth, interface count, and technology bucket names are not acceptance tests.

## Expose enforceable edges

Represent allowed dependencies with stable boundary identities, then use native visibility,
build, or import tools. Unsupported edges remain coverage gaps. A documented boundary and
an enforced boundary are different evidence states.

Before migration, identify public paths, generated references, registration/configuration,
and tests that follow the move. After migration, compare discovered consumers and edges
with the proposal.

**Done when:** contract ownership, implementation location, composition, and allowed edges
agree; each changed edge has a check or explicit gap. Formatting the tree is insufficient.
