# Component README contract

A **boundary README** is the short, co-located entry document for an intentional component. It
helps a human or fresh agent recover local purpose and constraints before reading implementation
details. It is not required for every physical directory.

## When it is warranted

Create or retain a boundary README when the directory is a real component and at least one of
these conditions applies:

- it has an independent responsibility, owner, lifecycle, build target, or public entrypoint;
- contributors repeatedly reconstruct the same local model;
- the component contains non-obvious dependency direction, ordering, compatibility, or safety
  invariants;
- the directory crosses an accepted structure-review trigger;
- parent documentation cannot describe the component without becoming a mixed inventory.

Treat generated, vendored, cache, build-output, and incidental container directories as
not-warranted unless they have a distinct workflow that readers must follow. A one-file component
can warrant a README when its boundary is important; a large homogeneous collection may not.

## Document roles

Keep each fact at its natural source:

| Source | Owns |
| --- | --- |
| repository README | project identity, first success, contribution entrypoints |
| architecture records | global relationships, durable choices, alternatives, consequences |
| boundary README | local purpose, navigation, invariants, verification, and pointers |
| `AGENTS.md` or equivalent | agent operating rules that apply automatically in the subtree |
| ownership files | reviewers and responsible teams or people |
| manifests/build/configuration | paths, targets, versions, dependencies, and executable commands |
| tests and sensors | observable behavior and boundary enforcement |

The README summarizes stable local meaning and links to these sources. It does not copy a full
ADR, package manifest, generated file list, or version matrix.

## Read order

When entering a component:

1. Read the nearest boundary README.
2. Read the nearest applicable agent instructions and ownership file.
3. Follow only the parent/global links needed by the current task.
4. Verify claims against code, build metadata, configuration, and tests before changing them.

A child README states the delta from its parent. Repeated parent prose belongs in the parent and
is reached through a relative link.

## Minimal shape

Adapt headings to repository style while retaining the meaning:

```markdown
# <Component name>

## Purpose
<Responsibility, intended consumers, and explicit non-goals.>

## Boundary
<Entrypoints, visibility, inputs/outputs, allowed dependencies, owner, and lifecycle.>

## Map
<A small concept-to-path guide for stable entrypoints, not an exhaustive file list.>

## Invariants
<Only constraints, ordering, compatibility, or failure rules not obvious from code.>

## Verify
<Canonical repository checks or links to their executable source.>

## Related
<Parent README, architecture records, ownership, and neighboring components.>
```

The opening should let a reader decide within a minute whether this is the correct component.
Keep the whole document readable in a few minutes. A README that accumulates several unrelated
purposes is itself a structure signal.

## Update triggers

Review the boundary README when one of these changes:

- component responsibility or non-goal;
- entrypoint, visibility, allowed dependency, or public path;
- owner, lifecycle, build unit, or verification route;
- path names referenced by the Map;
- an accepted architecture decision linked from the component;
- a migration creates, merges, splits, or removes the boundary.

Ordinary internal edits do not require README churn when these facts remain true. Use source and
test review for behavior details.

## Freshness sensors

Use the cheapest repository-native checks available:

- validate relative links and referenced local paths;
- confirm required boundary README coverage from the accepted Map or policy;
- flag README references to removed entrypoints, owners, or verification commands;
- review a README that grows beyond the repository's local size convention;
- detect duplicated parent sections where practical;
- require semantic review when a boundary-defining file changes.

Static checks can prove that links and paths resolve; they cannot prove that the prose still
describes the component. Give semantic review an owner and a trigger rather than claiming a link
check establishes correctness.

## Writing handoff

When `$readme-authoring` is available, pass it the accepted boundary, audience, fact ledger,
required headings, canonical sources, and target path. That skill owns the prose audit and README
validation. Repository structure owns the coverage decision and the relationship to the Map.
