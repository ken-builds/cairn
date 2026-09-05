---
name: repository-structure
description: Assess and evolve language-agnostic repository structure when adding or splitting components, a directory crosses growth signals, local context is missing, or ownership, dependency, build, visibility, or path boundaries need review.
---

# Repository Structure

Use this skill when a change adds or splits components, a directory is growing, a
component is difficult to understand from its path and code alone, or a path move
could affect ownership, dependencies, build targets, visibility, or public entrypoints.
It covers the physical tree, logical component boundaries, local context documents,
and the sensors that keep them aligned. It applies across languages and build systems.

The deliverable is a traceable **Structure Review**: a baseline, a Structure Map,
growth signals, component README coverage, candidate layouts, a decision or explicit
deferral, sensors, and a migration/rollback handoff. A threshold creates a review
question; it does not select a layout by itself.

## Boundary and authorization

Keep one authorization level active at a time:

- **design** - inspect the repository and produce a read-only review. Keep files and
  repository metadata unchanged.
- **probe** - after explicit authorization, run bounded inventory, history, or graph
  checks in the repository or a disposable copy. Record the command and limits.
- **record** - after explicit authorization, write a Structure Review, an accepted
  structure policy, a boundary README, or an ADR in the repository's established
  location.
- **migrate** - after explicit approval of the exact paths and target tree, move paths,
  update references and boundary metadata, and preserve behavior. Use a separate
  commit plan when the repository provides one.

Do not combine a path migration with an unrelated behavior change unless the approval
names both scopes. A public path, build target, data contract, runtime boundary, or
deployment change is an architecture-design handoff, not a directory-only decision.

## Stable vocabulary

Keep these leading words stable:

- **tree** - the physical directory and file hierarchy.
- **component** - a cohesive responsibility with a recognizable boundary.
- **boundary** - an ownership, visibility, build, lifecycle, or dependency line.
- **Map** - the evidence-backed table of components, paths, consumers, and allowed edges.
- **signal** - a measured structural clue such as growth, churn, or coupling.
- **trigger** - a signal combination that requires a review action.
- **candidate** - a concrete layout or keep-as-is option.
- **sensor** - an executable or observable check for a structural invariant.
- **waiver** - a time-bounded, owned decision to retain an intentional exception.
- **drift** - divergence between the accepted Map, local context, and repository tree.

Use `confirmed`, `inferred`, `unknown`, `not-run`, and `blocked` for evidence, probes,
and sensors. Keep one authoritative source for paths, commands, ownership, and durable
rationale; link from README files instead of copying volatile facts.

## Conditional references

Read only the references reached by the current branch:

- Read [structure-contract.md](references/structure-contract.md) before drafting,
  recording, or validating a Structure Review or structure policy.
- Read [signals-and-thresholds.md](references/signals-and-thresholds.md) when a directory
  grows, a file-count question is raised, or mixed responsibilities need classification.
- Read [component-readme-contract.md](references/component-readme-contract.md) when a
  boundary README is missing, stale, too long, or proposed as a first intervention.
- Read [sensors-and-adapters.md](references/sensors-and-adapters.md) when selecting
  dependency, visibility, ownership, history, or README drift checks.
- Read [migration-playbook.md](references/migration-playbook.md) before an approved path
  move, public-path compatibility change, or boundary metadata migration.
- Read [industry-patterns.md](references/industry-patterns.md) when external precedent
  or a comparison with a large repository is part of the decision.

Hand off README prose and link validation to `$readme-authoring` when available. Hand
off cross-module contracts, data, runtime, deployment, or durable architecture choices
to `$architecture-design`; hand off commit ordering and execution to `$git-commit-series`.
After implementation, use `$implementation-rationale` for non-obvious rationale or
compatibility findings that must survive the move.

## Workflow

### 1. Establish the baseline

1. Read repository-local instructions, contribution guidance, manifests, build and test
   entrypoints, CI, ownership files, architecture records, and the current tree.
2. Capture branch, `HEAD`, index/worktree status, untracked paths, and protected changes.
3. Identify the requested outcome, non-goals, affected roots, public paths, and active
   authorization level.

**Done when:** the protected state, scope, rule sources, and candidate roots are recorded;
no user change is treated as disposable.

### 2. Recover local context

1. From each target path, find the nearest `README.md`, `AGENTS.md`, ownership file,
   boundary manifest, and build/package marker.
2. Read the nearest local README first, then follow links to parent and global records.
3. Separate executable facts from prose summaries and list contradictions or missing
   context as explicit unknowns.

**Done when:** a fresh agent can name the local purpose, entrypoint, owner, verification
path, and missing context without scanning unrelated documentation.

### 3. Build the inventory

1. Count direct production files separately from tests, generated files, vendored files,
   documentation, tooling, and build output.
2. Measure physical or repository-native effective size, semantic depth, sibling fan-out,
   and optional version-control churn or co-change clusters.
3. Discover the repository's native dependency graph, package/build boundaries, public
   entrypoints, visibility rules, and ownership patterns. Prefer native reports over
   ad-hoc import parsing.

**Done when:** every reported measurement has a source, scope, and state; unsupported
measurements are `unknown` rather than inferred.

### 4. Construct the Map

For every in-scope component, record its path or glob, responsibility, non-goals, owner,
public entrypoint, visibility, allowed dependencies, consumers, lifecycle, tests, and
local README status. Distinguish a directory that is merely a container from one that
is a real boundary.

**Done when:** each candidate boundary has an owner and a purpose, every cross-boundary
edge is explainable, and unresolved edges have an owner or next check.

### 5. Classify signals and README coverage

1. Apply the soft growth bands and hard-boundary triggers in
   [signals-and-thresholds.md](references/signals-and-thresholds.md).
2. Decide whether the lowest-cost useful action is to retain the tree, add or revise a
   boundary README, add a sensor, or compare structural candidates.
3. Treat a missing README as a review signal only when the directory is an intentional
   boundary; ordinary folders do not receive documentation by quota.

**Done when:** every signal has a disposition of `retain`, `document`, `review`,
`migrate`, or `waive`, with evidence and an owner.

### 6. Compare candidates

Keep C0 as the current layout or smallest safe change. Add the smallest materially
different alternatives needed by the drivers, commonly:

- C0 - retain the current tree and add sensors or local context;
- C1 - group files by capability, feature, or subsystem boundary;
- C2 - create independent package, build, visibility, or ownership units;
- C3 - use local layer directories only where the dependency relation is stable and
  substantially one-way.

Compare cohesion, discoverability, dependency enforcement, public compatibility, build
and release impact, ownership, migration cost, rollback, and expected growth. Do not
use directory depth or a pattern name as a substitute for evidence.

**Done when:** the selected candidate, rejected alternatives, sensitivity points, and
revisit trigger are explicit.

### 7. Record and obtain approval

Use the repository's architecture Brief and ADR convention when one exists. Otherwise,
use the Structure Review contract and record only the rationale that cannot be derived
from the tree or build configuration. A structure policy is optional and should be
introduced only when a sensor needs a stable, machine-readable boundary declaration.

**Done when:** the record names exact paths, public-path effects, sensors, migration
phases, rollback, owners, and the next authorized operation.

### 8. Migrate in controlled increments

After approval, follow [migration-playbook.md](references/migration-playbook.md). Keep
path moves, reference updates, boundary metadata, and behavior changes reviewable. Update
local README links and ownership/build declarations in the same boundary change.

**Done when:** the target tree exists, all known references resolve, public compatibility
is addressed, and every migration step has a passing or explicitly classified gate.

### 9. Verify and monitor drift

Run the relevant sensors from [sensors-and-adapters.md](references/sensors-and-adapters.md),
then compare the resulting tree, Map, README coverage, dependency edges, and ownership
with the accepted record. Record drift as a new decision or an owned waiver.

**Done when:** every critical invariant has a passing sensor or an owner, cadence, repair
path, and expiry; the handoff distinguishes confirmed, inferred, unknown, not-run, and
blocked work.

## Response handoff

Return a compact index containing:

- baseline, protected changes, scope, and authorization level;
- Structure Map and signal/README coverage summary;
- candidates, selected or deferred option, and trade-offs;
- Evidence, Probe, Sensor, and waiver states;
- migration and rollback sequence, if authorized;
- open questions with owners and next checks;
- the exact next authorization required.

The Structure Review, repository configuration, code, and tests remain the sources of
truth. The response is an index, not a duplicate architecture document.
