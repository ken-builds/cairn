# Structure migration playbook

Use this playbook only after the target paths, candidate, public-path policy, and rollback point
have explicit approval. A directory move is a repository-wide change even when runtime behavior
is intended to remain constant.

## 1. Freeze the migration boundary

Record the baseline revision, protected worktree changes, source and destination paths, affected
entrypoints, owners, build units, generated outputs, documentation links, and excluded behavior
changes. Confirm whether every moved path is private, internal, or public to a consumer.

**Done when:** an independent reviewer can list exactly what will move and what will remain.

## 2. Prepare a characterization gate

Run the narrowest existing checks that describe current behavior and public compatibility. If the
repository lacks a useful check, record that gap and add it only when separately authorized. Use a
disposable copy for experiments that install tools or create generated output.

**Done when:** the baseline checks, environment, and limitations are recorded as passed, failed,
not-run, or blocked.

## 3. Move paths without changing behavior

Use the repository's version-control-aware move operation. Keep naming changes, formatting, API
changes, and cleanup separate from the path move unless they are required to make the tree build.
Preserve tests, fixtures, documentation, generated-source declarations, and ownership metadata in
their intended relationship to the boundary.

**Done when:** the destination tree contains the approved files and the diff shows no unrelated
behavioral edit.

## 4. Repair references and boundary metadata

Update source references, include/import paths, build descriptions, package or visibility metadata,
registries, configuration, scripts, ownership files, documentation links, and generated indexes.
Search the whole repository for the old path and classify every remaining match. Keep a compatibility
alias, redirect, shim, or deprecation window when a supported public path must remain stable; record
an explicit breaking decision when it cannot.

**Done when:** every old-path match has a disposition and all accepted boundary edges use the new
path or boundary ID.

## 5. Update local context

Create or revise the boundary README according to
[component-readme-contract.md](component-readme-contract.md). Link to global records and executable
commands instead of copying them. Update ownership and agent instructions only when their scope
changed.

**Done when:** a fresh agent can enter the new path, understand its purpose and constraints, and
reach the canonical verification path without reading unrelated directories.

## 6. Verify in widening gates

Run, in repository order:

1. path/link and formatting checks;
2. dependency-cycle and boundary checks;
3. focused tests for moved components;
4. package/build/type/schema checks supplied by the repository;
5. public consumer, installation, or release checks when paths are exposed;
6. the full required gate and a clean-output check.

Record command, environment, result, and limitation for each gate. A passing build proves
buildability, not that the chosen boundary is cohesive; keep the structural review open until the
Map and sensors agree with the resulting tree.

**Done when:** all required gates pass or have an explicit not-run/blocked disposition, and no
unclassified old-path or public-compatibility issue remains.

## 7. Commit and rollback

Use `$git-commit-series` when available. A reviewable default series is:

1. accepted policy/README and sensor changes;
2. path-only move and reference repair;
3. required boundary-rule or build metadata updates;
4. separately authorized behavior or cleanup changes.

Keep the rollback point before the first path move. If a gate fails, revert or repair the smallest
approved increment, preserve the failure evidence, and re-plan when the target tree or scope changes.

**Done when:** each increment has one intent, a green gate, an owner, and a reversible outcome.

## 8. Reconcile drift

Compare the final tree with the accepted Structure Map, README coverage, ownership, dependency
edges, public paths, and candidate rationale. If the intended structure changed, write a new
decision or superseding review rather than silently editing history.

**Done when:** the final handoff names the resulting tree, sensors, rollback effect, residuals, and
the next review trigger.
