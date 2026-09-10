# Probes and benchmarks

Use this reference when a design claim cannot be settled by repository inspection or
documentation and the result could change the candidate ranking. A probe is a small
decision instrument, not a miniature production system.

## Trigger and choose the smallest probe

Trigger a probe for a named unknown involving:

- performance, capacity, latency, memory, cost, or scalability;
- concurrency, ordering, consistency, retries, or failure recovery;
- API, schema, runtime, platform, or dependency compatibility;
- integration wiring, deployment, observability, or operational feasibility;
- a data structure or algorithm whose behavior affects a hard driver.

Choose the least expensive experiment that can distinguish the candidates:

| Risk | Smallest useful probe | Escalate when |
| --- | --- | --- |
| API or build compatibility | compile, contract test, or migration fixture | transitive/runtime behavior differs |
| End-to-end wiring | walking skeleton or tracer bullet in a scratch app | lifecycle, failure, or deploy behavior is unknown |
| Latency/throughput | controlled benchmark against a baseline | tail, saturation, or workload sensitivity matters |
| Failure/recovery | targeted fault injection | recovery depends on distributed timing |
| Concurrent state or protocol | model/property test | state space or invariant needs exploration |
| Data migration | copy of representative schema/data and rollback rehearsal | volume, lock, or compatibility window is uncertain |

Do not select a tool because it is fashionable. Select it because its output can answer a
driver with a threshold.

## Authorization and isolation

Read-only inspection and lightweight checks that leave the repository and external systems
unchanged can remain at the `design` level. Before creating or modifying experiment files,
installing/upgrading dependencies, running load or fault injection, or mutating external
state, confirm the operation fits the user's probe authorization, reusing scope already
given. Ask only when the operation or budget exceeds it. Put
all mutable state in one of these boundaries:

1. a disposable Git worktree created from the recorded baseline;
2. a temporary directory or scratch project outside the repository; or
3. a container/ephemeral environment with a documented input snapshot.

Keep production systems, shared databases, credentials, real deployment targets, and the
main worktree out of the experiment. Pin or record dependency versions and environment
variables. Set a time, compute, request, and cost budget. If isolation or authorization is
unavailable, produce a `not-run` or `blocked` Probe record instead.

## Experiment card

Write this card before running the experiment:

```text
P<id>: <short name>
Question: <decision this probe can change>
Hypothesis: <falsifiable statement>
Candidates: <baseline and alternatives>
Workload/input: <representative shape, size, distribution, and concurrency>
Environment: <hardware, OS, runtime, dependency versions, configuration>
Baseline: <current implementation and measurement>
Method: <commands, harness, warm-up, repetitions, isolation>
Budget: <time, iterations, requests, resources, and cost>
Threshold: <pass/fail rule tied to a driver>
Result: <observations and raw artifact link>
State: confirmed | inferred | unknown | not-run | blocked
Limitations: <confounders, variance, missing coverage>
Cleanup: <what was removed and how>
Follow-up: <decision, sensor, or next experiment>
```

Keep raw commands and outputs available when they materially support the conclusion. A
probe can disprove a candidate without proving the winner; state that distinction.

## Benchmark minimums

For a performance result, record:

- the workload, input distribution, concurrency, and success/error criteria;
- hardware, operating system, runtime, compiler, dependency versions, and configuration;
- warm-up and cache state, repetitions, sample count, and duration;
- baseline and candidate measurements under comparable conditions;
- p50/p95/p99 (or a justified alternative), throughput, error rate, and variance;
- utilization, saturation, and resource limits that explain the result;
- whether the measurement includes queueing, retries, serialization, network, and startup;
- known measurement bias such as coordinated omission, noisy neighbors, or insufficient
  tail samples.

Use Little's Law or a queueing model only with clearly stated assumptions. A single fast
run, an average without a distribution, or “it compiles” is not a performance acceptance
test.

## Failure, compatibility, and data probes

For failure probes, state the injected fault, timing, expected invariant, observed response,
recovery time, data loss/duplication, and residual risk. For compatibility probes, test the
old and new producer/consumer or schema across the intended compatibility window, including
rollback. For data migrations, use representative shape and volume, measure locks and
backfill time, and rehearse abort and restore paths.

For concurrent protocols, use a small model, invariant/property test, or fault-injection
run when it can expose a concrete race. TLA+, Alloy, QuickCheck, Jepsen, and similar tools
are conditional instruments; their presence in a report is not itself evidence of safety.

## Result and cleanup gate

Classify the result:

- `confirmed` — the threshold was tested under the stated conditions;
- `inferred` — evidence supports the claim but leaves a material untested assumption;
- `unknown` — the experiment was inconclusive;
- `not-run` — a prerequisite or authorization was absent;
- `blocked` — a safety, access, or environment constraint prevented the run.

Delete disposable state or record why it must remain. Link the result to the candidate
matrix, update the risk, and add a Sensor when the property must stay true after merge.

**Done when:** the card, commands, conditions, threshold, result state, limitations, and
cleanup are all present, and the candidate decision cites the probe without overstating it.
