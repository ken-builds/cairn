# Design judgment

Read the branch reached by a proposed decision. Keep findings in the existing Map,
candidate comparison, or open questions; this reference requires no additional artifact.

## Decision-changing premises

Start with the changed flow and its producers, consumers, and effects. For a premise
that can alter a candidate, identify what would contradict it and where to look.

| Observed change | Inspect before choosing | Discriminating question |
| --- | --- | --- |
| Retry, timeout, fallback | caller retries, side effects, error contract | Can the operation have succeeded despite this failure signal? |
| Cache, snapshot, derived state | authoritative source, invalidation, trust boundary | Can a valid-looking result be stale or forged? |
| Multiple writes or state plus external effect | commit order, transaction scope | What remains committed after interruption at each boundary? |
| Shared resource or lifecycle | ownership, cancellation, concurrent consumers | Who still uses it after stop, timeout, or transfer? |
| Dependency/protocol replacement | actual versions, consumers, configured wiring | Which promised behavior depends on the old implementation? |

These are routing examples, not a universal questionnaire. Follow risks reached by the
scoped flow; add questions when discovered edges change the failure model. Prefer repository
evidence, then a targeted source lookup, then a bounded probe. Give unresolved premises their
impact, next check, and stopping condition. Reversible defaults can proceed within scope
when their impact is explicit; missing intent that changes the choice needs user input.

**Done when:** each discovered premise capable of changing the decision is supported,
rejected, or explicitly unresolved. State the investigation boundary rather than claiming
this enumeration exhausts unknown unknowns.

## Abstraction ownership

For each introduced or relocated abstraction, identify the consumer's required behavior,
the decision it hides, its current/planned implementation, and where concrete assembly occurs.
Locate the contract with the capability that owns its meaning using native language mechanisms.
A runtime-related contract can belong to a stable model boundary even when its implementation
belongs elsewhere.

Test substitution: name a plausible change supported by a current driver, the parts expected
to change, and consumer behavior expected to remain stable. A test seam or trust boundary
can justify an abstraction without two production implementations. If no driver needs the
separation, keep concrete code with a revisit trigger. File moves and interface counts are
not evidence of a protected boundary.

**Done when:** each affected abstraction names its owner, consumers, hidden variation,
assembly point, and substitution impact, or is deferred. Dependencies protect these relations
rather than following labels such as model/service/runtime.

## Failure responsibility

For changed failure paths, identify where validity is established, effects already committed,
the layer with enough context to recover, and the caller/operator observation path. Distinguish
absence, contract violation, transient failure, cancellation, and uncertain completion when
they require different actions.

Validate at trust/ownership boundaries and rely on established internal invariants. Retain
guards that enforce real contracts. Give recovery explicit triggers, budgets, and outcomes.
Sanitize sensitive payloads while preserving the safe category and stage needed for action.

**Done when:** recovery accounts for the changed failure categories, committed effects,
owner, and observation path. Uncertainty about the system becomes an evidence task rather
than silently widening supported runtime states.
