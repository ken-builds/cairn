# Structure signals and thresholds

Use structural metrics as sensors. They focus attention; semantic cohesion, ownership,
dependency evidence, and migration risk decide the response.

## File roles

Classify files before counting them:

- **production** - implementation, schema, resource, or configuration used by the product;
- **test** - tests, test support, examples used only by tests, and fixtures;
- **generated** - derived files whose generator is the source of truth;
- **vendor** - third-party or mirrored material maintained outside the component;
- **documentation** - README files, guides, references, and decision records;
- **tooling** - development, release, migration, and repository automation;
- **build output** - disposable compiler, package, cache, and report products.

Count direct files and recursive descendants separately. A direct-file signal answers whether
one directory presents too many peers. A recursive count describes subsystem size and cannot
by itself justify another directory level.

## Seed bands

Use these only when the repository has no accepted threshold:

| Direct production files | Initial disposition |
| --- | --- |
| fewer than 8 | keep the flat layout as the default candidate |
| 8 through 11 | observe growth and review on the next expansion |
| 12 through 19 | complete a Structure Review before further expansion |
| 20 or more | compare at least two materially different candidates |

Calibrate the bands after the first audit. Compare directories with the same role and semantic
level; record the median, upper percentile, and deliberate outliers. Keep an absolute floor so
a tiny repository does not turn every four-file folder into a component.

## Independent soft signals

Treat each category as one signal even when several metrics describe it:

- **growth** - direct peer count, text size, sibling fan-out, or sustained expansion;
- **cohesion** - more than one stable responsibility, vocabulary cluster, or reason to change;
- **coupling** - high cross-cluster traffic, broad fan-in/fan-out, or repeated coordination;
- **history** - distinct co-change clusters, concentrated churn, or large mixed review surfaces;
- **ownership** - unrelated owners, review paths, security scopes, or release cadences;
- **navigation** - ambiguous bucket names, repeated rediscovery, or excessive semantic depth;
- **context** - a stable component boundary lacks a concise local entry document.

One soft signal prompts observation. Two independent soft signals require a Structure Review.
A single high-confidence cohesion, ownership, or repeated-rediscovery signal may justify a review
before the seed file count is reached.

## Hard-boundary triggers

Start a Structure Review regardless of size when evidence shows:

- a dependency cycle or an edge forbidden by an accepted boundary;
- a public entrypoint or supported path could change without a compatibility decision;
- a build/package/visibility unit disagrees with the intended component boundary;
- security, data, lifecycle, or ownership responsibilities are mixed without one owner;
- a path move would invalidate repository automation, deployment, generated references, or
  downstream consumers;
- local documentation asserts a boundary that code, build metadata, or ownership contradicts.

Route runtime, data, deployment, or public-contract choices to architecture design. A structure
review may expose those questions; it does not settle them by renaming paths.

## Candidate actions

Select the least costly action that addresses the observed problem:

- `retain` - the directory is cohesive and navigable; preserve it;
- `document` - add or repair a boundary README or ownership pointer before moving code;
- `review` - compare layouts and sensors without changing the tree;
- `migrate` - apply an approved boundary move with compatibility and rollback;
- `waive` - retain a deliberate exception with an owner and revisit trigger.

A homogeneous registry, driver collection, migration set, or fixture catalog can remain large
when naming, ownership, lifecycle, and generated status are clear. Conversely, a small directory
can need separation when its files cross a hard boundary.

## Depth and naming

Count semantic segments rather than boilerplate roots such as `source` or `packages`. Review
depth when a path contains more concepts than a reader can name consistently, when a directory
exists only to hold one child without adding policy, or when dependency levels are encoded as
numbers that will shift as the graph evolves.

Prefer names already present in domain, subsystem, ownership, or build vocabulary. Generic
buckets earn their place only when they represent a stable shared responsibility with an owner
and entry policy.

## Waiver contract

Every waiver records:

- the boundary and signal;
- the observed value and evidence;
- why the current structure remains coherent;
- owner and approval;
- expiry date or observable revisit trigger;
- the sensor and failure action.

An expired waiver re-opens the review. A waiver for file count does not waive cycles, public-path
compatibility, or security/ownership conflicts.
