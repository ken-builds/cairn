# Commit boundary rules

Use this reference while building the hunk ledger and the dependency DAG. It
defines the decisions that make a series reviewable without turning a commit
into an arbitrary slice of the final diff.

## Working vocabulary

- **Intent**: the single reviewer question answered by a commit. Phrase it as
  “why does this commit exist?” in one sentence.
- **Atomic change**: the smallest set of hunks that can be understood,
  validated, and reverted without borrowing an unrelated intent.
- **Hunk ownership**: the ledger assignment of each changed region to exactly
  one atomic change, or to a protected, excluded, undecided, or residual bucket.
- **Coupling**: a relationship that makes two hunks require one another for
  compilation, runtime behavior, tests, migration safety, or review
  comprehension.
- **Green commit**: a public commit whose repository-required build and
  relevant checks pass at that point in the series.

## Boundary decision

Apply these questions in order:

1. What user, maintainer, or operational problem does this hunk address?
2. Can a reviewer explain the hunk without understanding another candidate?
3. Can the hunk be built and tested at the proposed point?
4. Can it be reverted without removing an unrelated behavior or safety fix?
5. Does repository policy require it to travel with a manifest, lockfile,
   generated result, migration, or test?

Split when the answers identify different intents and the resulting commits
remain green and understandable. Merge when coupling makes a split misleading,
unbuildable, untestable, or unsafe to revert. Record the reason in the plan.

## Default boundary matrix

| Change shape | Default boundary | Merge or split adjustment |
| --- | --- | --- |
| Behavior change plus direct regression or acceptance tests | One commit | Keep tests with the behavior; split only independent test infrastructure. |
| Pure refactor, rename, or mechanical migration | Separate commit | Merge with behavior only when the refactor is inseparable and the repository convention treats it as one change. |
| Formatting or generated formatting noise | Separate commit | Keep with behavior when the formatter is an unavoidable part of the same build gate and the repository expects that shape. |
| Independent documentation or examples | Separate commit | Keep with an API/behavior commit when the documentation is required to make that change usable or reviewable. |
| Dependency manifest and lockfile | Usually one commit | Follow the package manager and repository policy; split only when the lockfile update is independently intentional. |
| API or schema migration | Expand/compatibility → callers or data migration → contract/cleanup | Collapse stages only when compatibility is guaranteed and every intermediate point remains green. |
| Generated source and its generator/input | Follow repository policy | Keep the generated result with the source change when consumers need both; identify generator-only changes separately when reproducible. |
| Test fixture or harness change | Separate if reusable | Keep with the feature when the fixture exists only to express that feature's direct test. |
| Bug fix and opportunistic cleanup | Separate | Keep only the fix's required cleanup; classify unrelated cleanup as residual or a separate intent. |
| Debug logging, temporary files, experiments, or WIP | Exclude or protect | A user may explicitly promote one to a planned intent after its purpose is clear. |
| Rename with edits | Rename-only → behavior edits when useful | Keep together when separating would destroy history or make review harder; state the tradeoff. |
| Binary or opaque artifact | Treat as a whole-file hunk | Require repository policy and a review/verification story; otherwise mark the hunk undecided. |

The matrix is a default, not a substitute for repository evidence. A local
contribution guide, hook, release process, or recent history overrides it.

## Tests and green states

Keep a test in the same commit when it directly proves the behavior introduced
or fixed there. Keep a test-only refactor, framework upgrade, fixture cleanup,
or broad test migration separate when it has an independent intent.

The public series should be green at each point whenever the repository can
support that property. If a migration necessarily crosses a temporary
incompatibility, choose a compatibility design, combine inseparable hunks, or
mark the repository-approved exception explicitly. A red point caused only by
the desire for more commits is not an atomic boundary.

## Hunk-level ownership

Give each ledger entry a stable ID and an anchor that another agent can locate:
path plus old/new line range, symbol, or a short patch summary. Add a
normalized patch/context fingerprint when available. A file path is not
sufficient when one file contains several intents.

When one textual hunk contains two intents:

1. Inspect nearby context and use patch-level staging or a semantic split if
   the separation is safe.
2. If the split would change meaning, move the whole hunk into the coupled
   intent and explain why.
3. If ownership remains genuinely ambiguous, mark the hunk undecided and stop the
   affected plan item; do not assign the hunk twice or silently discard it.

An untracked file is one whole-file hunk unless its contents can be separated
without inventing a misleading intermediate state; inspect its content rather
than relying on the default tracked-file diff. Binary files, submodules, mode
changes, and renames receive explicit ledger entries even when no textual patch
is available. For mixed staged and unstaged changes, compare both deltas with
HEAD and keep index and worktree ownership distinct.

## Common dependency edges

Create an edge only when the successor relies on the predecessor's code,
schema, behavior, or validation setup. Typical edges are:

- behavior-neutral refactor → implementation or fix;
- reusable fixture/harness → tests that consume it;
- API/schema expansion or compatibility layer → callers/data migration;
- callers/data migration → removal of the old contract;
- source or generator update → required generated output;
- dependency or toolchain update → code that requires the new version.

Topological order is a consequence of these edges. File order, authoring order,
and commit-message type are not dependencies. For independent intents, use a
deterministic tie-break: repository history or stack convention first, then
review/rollback risk, then stable ledger order; record the tie-break in the
plan.

## Review and rollback checks

For each candidate, ask:

- Can a reviewer summarize its purpose without reading future commits?
- Does its diff contain only evidence for that purpose?
- Is its validation proportionate and reproducible?
- Would reverting it leave the repository in a comprehensible state?

When a candidate fails one of these checks, first merge the coupled hunk or
split the unrelated hunk; changing only the subject line does not repair a
bad boundary.

## Boundary smells

Flag these in the plan when they appear:

- a commit whose reason says “and also”;
- a test that is expected to fail until a later commit;
- a large formatting diff hiding behavior;
- a cleanup that is justified only because the file was already open;
- a generated or lockfile change with no source or policy explanation;
- a candidate that owns a path but not the hunk that actually changes its
  behavior;
- a dependency edge inferred only from chronological editing order.
