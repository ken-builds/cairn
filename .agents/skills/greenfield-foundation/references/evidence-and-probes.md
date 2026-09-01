# Evidence and probes for greenfield foundations

Use this reference when a fact can change the foundation choice. The goal is a bounded evidence
ledger and a small decision instrument, not an exhaustive technology survey.

## Claim triage

Classify every material statement before relying on it:

| Class | Example | Treatment |
| --- | --- | --- |
| Supplied/project fact | The sponsor requires a regional data boundary. | Cite the supplied requirement or owner. |
| Stable principle | A boundary should hide a decision likely to change. | Treat as a heuristic; cite a stable source only when it changes the ranking. |
| Dynamic external fact | A package version supports a required runtime or fixes a vulnerability. | Verify an official source and record version/date. |
| Measurement | Candidate B meets the p95 or cost threshold. | Run a reproducible probe and preserve conditions and raw output. |
| Inference | A managed service may reduce on-call load for this team. | Connect supporting facts and label confidence. |

Never turn memory, a search-result snippet, a vendor slogan, or an unconditioned benchmark into
confirmed evidence.

## Source order

For dynamic claims, prefer:

1. official API/reference documentation and compatibility matrices;
2. official release notes, migration guides, security advisories, and support policies;
3. official issue, pull request, design note, or fixing commit;
4. reproducible local inspection or an isolated probe;
5. a reputable secondary source only to discover what must be verified above.

Record the exact claim, source URL/path/command, project or package, version/commit, access date,
environment, applicability, state, inference, and next check. Check the proposed version against
the target project's manifest and lockfile when they exist.

## Authorization and isolation

- Read-only inspection and documentation lookup remain at `design`.
- Creating experiment files, installing or upgrading dependencies, running load or fault tests,
  or touching an external service requires explicit `probe` authorization.
- Keep mutable state in a disposable directory, scratch project, isolated container, or approved
  temporary worktree. Keep credentials, production systems, shared databases, and the real target
  repository outside the experiment.
- Pin or record versions and configuration. Set time, compute, request, and cost budgets.
- Never print secret values. If a prerequisite or authorization is absent, record `not-run` or
  `blocked` with the exact safe next action.

## Experiment card

Write the card before running a probe:

```text
P<id>: <short name>
Question: <decision this probe can change>
Hypothesis: <falsifiable statement>
Candidates: <baseline and alternatives>
Workload/input: <shape, scale, distribution, and concurrency>
Environment: <OS, runtime, versions, configuration, and hardware>
Baseline: <reference behavior or measurement>
Method and budget: <commands, warm-up, repetitions, timeout/cost, cleanup>
Threshold: <driver-linked pass/fail rule>
Result and artifact: <observation and link>
State: confirmed | inferred | unknown | not-run | blocked
Limitations: <confounders, variance, missing coverage>
Follow-up: <decision, sensor, or next experiment>
```

Choose the smallest experiment that distinguishes candidates:

| Unknown | Smallest useful probe |
| --- | --- |
| API/build compatibility | Compile, contract test, or migration fixture in a scratch copy. |
| End-to-end wiring | A walking skeleton with disposable dependencies. |
| Latency/throughput/cost | Controlled benchmark against C0 with a stated distribution and budget. |
| Failure/recovery | Targeted fault injection with recovery and data-loss observations. |
| Concurrent ordering/consistency | Small model, property test, or bounded concurrency run. |
| Data initialization/rollback | Representative fixture plus abort/restore rehearsal. |

## Measurement minimums

For performance or capacity evidence, record workload, success/error criteria, hardware, runtime,
configuration, warm-up, cache state, repetitions, p50/p95/p99 (or a justified alternative),
throughput, error rate, variance, utilization/saturation, resource limits, and known measurement
bias. A compile-only spike proves feasibility, not quality or capacity.

For failure, compatibility, or data probes, record the injected condition, expected invariant,
observed response, recovery time, duplication/data-loss behavior, compatibility window, and
residual risk.

## Result and stopping gate

Classify the result as:

- `confirmed` — the threshold was tested under the stated conditions;
- `inferred` — evidence supports the claim but leaves a material assumption;
- `unknown` — the experiment was inconclusive;
- `not-run` — a prerequisite or authorization was absent;
- `blocked` — a safety, access, or environment constraint prevented the run.

Stop research when every decision-changing claim is confirmed, rejected by evidence, or explicitly
tracked with a next check and owner. Longer bibliographies without a new decision signal are
sediment.
