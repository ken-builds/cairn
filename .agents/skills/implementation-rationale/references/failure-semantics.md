# Failure semantics during implementation

Use on changed guards, exception handling, fallback/retry, lifecycle, or compatibility paths.
Inspect the scoped diff and affected call/implementation sites. Record decision-relevant
findings in the existing ledger; routine branches need no new comments or tables.

## Establish the contract

For each discovered changed path, determine:

1. Where validity was established and what callers may rely on.
2. Which failure can reach the path, including cancellation or uncertain completion.
3. Which state or external effects may already be committed.
4. Which layer owns recovery and what permits a safe retry or alternative result.
5. How callers/operators observe the outcome and what checks distinguish the cases.

Verify upstream validation, retry, and lifecycle behavior instead of inferring it from a
type or comment. Resolve uncertainty through inspection or a focused probe before changing
supported runtime states. Ask for a missing policy only when it materially changes behavior.

## Choose a disposition

| Established condition | Implementation direction |
| --- | --- |
| Untrusted input | Validate at its owning boundary and return the defined failure. |
| Internal invariant already guaranteed | Rely on it or assert a violation explicitly. |
| Expected absence | Return the absence form defined by the consumer contract. |
| Transient failure with safe replay | Retry at the owning layer within its budget, accounting for upstream retries. |
| Effect may have committed | Reconcile or deduplicate before retrying; preserve ambiguity in the outcome. |
| Cancellation, stale ownership, shutdown | Settle using the lifecycle/ownership contract. |
| Recovery itself fails | Preserve a safe category/stage and observation path; identify who can recover next. |

Choose from the observed contract, not the spelling of a catch or guard. Catch only as
broadly as recovery covers. An observer may be best-effort when its failure is explicitly
allowed not to affect settlement. Sanitized errors can omit raw payloads while preserving
categories/stages needed to distinguish provider, storage, transport, and policy failures.

## Verify before documenting

Exercise failure classes requiring different actions. If recovery assumes an expired lease,
also consider a storage failure that is not expiry: a comment about expiry cannot justify
swallowing both. Check promised normal results and failure dispositions through observable
behavior rather than tests that mirror individual branches.

Place public behavior at declarations, non-obvious reasons beside recovery boundaries, and
multi-file findings in an Implementation Record when warranted.

**Done when:** changed paths have evidence for reachable conditions, committed effects,
recovery ownership, and outcomes, or explicit questions. Tests and comments distinguish
the cases the contract treats differently.
