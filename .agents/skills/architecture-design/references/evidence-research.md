# Evidence and dependency research

Use this reference whenever a design depends on facts that can change: framework or
library behavior, supported versions, release notes, security advisories, protocol rules,
compatibility promises, ecosystem practice, or a claim about current performance. The
goal is a bounded evidence ledger, not an exhaustive internet survey.

## Claim triage

Classify each statement before researching it:

| Class | Example | Required treatment |
| --- | --- | --- |
| Repository fact | the lockfile resolves package `x` to version `v` | inspect the repository and cite the path/command |
| Stable principle | information hiding reduces coupling | use a stable source when it changes the candidate; label it as a heuristic |
| Dynamic external fact | version `v` fixes a race or supports an API | verify an official source and record version/date |
| Measurement | candidate B has p95 below the target | run a reproducible probe and retain its conditions |
| Inference | an upgrade is likely to remove a workaround | connect the supporting facts and state confidence |

Only the last three can change the ranking through new evidence. Keep them separate in
the Brief so a later agent can update one claim without rewriting the design.

## Source order

Use the strongest source available for the exact claim:

1. Official API/reference documentation and compatibility matrix.
2. Official release notes, changelog, migration guide, security advisory, or support
   policy for the exact version.
3. Official issue, pull request, design note, or fixing commit when behavior is not yet
   reflected in documentation.
4. Reproducible local source inspection or an isolated probe.
5. A reputable secondary source for discovery or context, followed by verification above.

Search results, forum answers, old blog posts, benchmarks without conditions, and memory
are leads. They are not final evidence for a changing claim.

## Evidence record

Create one row per decision-changing claim. Use this shape in the Brief:

```text
E<id>
Claim: <precise statement that could be true or false>
Source: <official URL, file/symbol, command, or probe artifact>
Project/package: <name>
Version or commit: <exact version, tag, or SHA; “not stated” is explicit>
Accessed or measured: <YYYY-MM-DD>
Environment: <runtime, platform, configuration, or scope>
State: confirmed | inferred | unknown | not-run | blocked
Applicability: <why this source applies to this repository>
Inference: <reasoning from the source, or “none”>
Next check: <command, query, owner, or revisit date>
```

For a web source, preserve the URL and the relevant heading or section. For a local
source, preserve the path and symbol or command. For a probe, link the experiment card
and result rather than paraphrasing numbers without conditions.

## Dependency and upstream-fix gate

When a dependency is involved, walk this sequence:

1. Identify the local package, resolved version, transitive path, runtime, and affected
   behavior from manifests and lockfiles.
2. State the defect or capability as a minimal reproduction or precise claim. Search the
   upstream tracker and release history using the exact package and version.
3. Check for an official fixed release, backport, migration note, or supported configuration.
   Prefer that path when its compatibility and rollback cost fit the drivers.
4. Compare four options explicitly: remain on the current version, upgrade, use a supported
   workaround, or carry a patch/fork. Include API/ABI compatibility, transitive changes,
   security and license impact, build/reproducibility, operational rollout, and rollback.
5. If a workaround, patch, or fork wins, record its owner, minimized surface, upstream
   issue/PR, exit condition, and date or version at which it must be re-evaluated.
6. Validate the selected option in an isolated copy before changing the real manifest or
   lockfile. Keep dependency changes and product-code changes separately reviewable.

Use a table such as:

| Option | Upstream status | Compatibility | Security/license | Migration/rollback | Evidence | State |
| --- | --- | --- | --- | --- | --- | --- |
| Current | <known behavior> | <impact> | <impact> | <effect> | E1 | confirmed |
| Upgrade | <fixed version> | <impact> | <impact> | <effect> | E2 | inferred |
| Workaround | <supported?> | <impact> | <impact> | <effect> | E3 | confirmed |
| Patch/fork | <maintenance path> | <impact> | <impact> | <effect> | E4 | unknown |

An automated update proposal, vulnerability score, or ecosystem trend is a signal. The
decision still needs semantic compatibility evidence and a rollback path.

## Network and access boundaries

Use the host's network policy and allowlist. Keep requests narrow and prefer official
domains. Use `blocked` when a request was attempted but access was denied by policy,
authentication, or an unavailable endpoint; include the URL, reason, and safe command a
user can run. Use `not-run` when the query was not attempted because network access,
authorization, or a prerequisite was unavailable. Continue local mapping in either case;
do not fill in current versions from memory.

External research never authorizes a repository mutation. Dependency installation, lockfile
updates, patches, and forks belong to the `probe` or `record` level and require the explicit
authorization described in the main skill.

## Research stopping rule

Stop when every claim that could change the selected candidate is one of:

- `confirmed` by a source or reproducible observation;
- `rejected` with the evidence that rules it out; or
- `unknown`, `not-run`, or `blocked` with a concrete next check and an owner.

Record diminishing-return questions as deferred work. A longer bibliography without a new
decision signal is sediment, not architecture evidence.
