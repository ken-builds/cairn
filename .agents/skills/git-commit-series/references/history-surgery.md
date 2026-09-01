# Local history surgery

Read this reference only for history-edit mode: splitting, reordering,
squashing, or fixing commits that already exist. It does not replace the
hunk-ledger rules for a new worktree diff.

## Scope and preflight

Identify the exact rewrite range, old tip, intended new tip, upstream or
tracking ref, and whether any commit has been published. Published history,
protected branches, signed commits, merge commits, submodules, and
subtree/vendor boundaries require an explicit risk decision.

Begin with a clean index and worktree, or establish an approved isolated
preservation strategy for protected changes before starting rebase. A rebase
must not absorb unrelated staged or unstaged work.

Record before rewriting:

~~~sh
git status --short --branch
git rev-parse HEAD
git log --graph --oneline --decorate <base>..HEAD
git show-ref --heads --tags
~~~

Create a named backup ref at the old tip before mutation when the user has
authorized that safety step. Record its name in the handoff. A backup ref is
not permission to rewrite a remote or to force-push it.

**Preflight is complete** when the range, publication status, merge shape,
backup strategy, and desired final series are explicit.

## Splitting one existing commit

Use an interactive rebase over the parent of the target commit and mark the
target for edit. At the edit stop, expose the commit's changes, then stage and
commit the planned hunk groups in dependency order.

~~~sh
git rebase -i <target-parent>
# mark the target as edit
git reset HEAD^
# stage one planned group at a time
git add -p -- <path>
git diff --cached --check
git commit
git add -p -- <path>
git diff --cached --check
git commit
git rebase --continue
~~~

Use the exact message and ownership from the revised CommitPlan. If one hunk
cannot be separated without changing semantics, keep it with its coupled
intent and update the plan rather than manufacturing a misleading commit.

## Reordering, squashing, and fixups

Reorder only commits whose intents and dependencies permit the new order.
Squash or fixup commits that express one intent or whose repository policy
requires a single public commit. Keep the logical series clear before applying
a final release-oriented squash.

For local corrections, a fixup commit can target an earlier commit and then be
folded with autosquash when that rewrite is authorized:

~~~sh
git commit --fixup=<target>
git rebase -i --autosquash <base>
~~~

Review the generated todo list before accepting it. Do not use autosquash to
hide an unrelated intent or to bypass a failed validation gate.

## Merge commits and metadata

Use rebase-merges when merge topology is part of the intended history. A
linear interactive rebase can discard meaningful merge structure. Rewriting
changes commit IDs and normally invalidates signatures; preserve authors,
trailers, co-authorship, and sign-off requirements according to repository
policy, then re-check hooks.

## Conflicts and recovery

At every stop, inspect the conflict set and compare it with the plan. Resolve
only the named scope, run the relevant gate, and continue. If the operation no
longer represents the plan, use the native abort path and return to planning.

~~~sh
git status
git rebase --abort
git reflog
~~~

The reflog and the named backup ref are recovery aids; report them in the
handoff. Never delete a recovery ref or use reset/clean to discard work unless
the exact target has separate authorization.

## Verification

After rewriting, compare old and new series with range-diff and inspect the
final status:

~~~sh
git range-diff <old-base>..<old-tip> <new-base>..<new-tip>
git log --graph --oneline --decorate <new-base>..<new-tip>
git diff --stat <new-base>..<new-tip>
git status --short --branch
~~~

Run each plan gate at the relevant rewritten commit or at the repository's
approved aggregate point. Report changed hashes, dropped or added hunks,
metadata differences, validation results, and the backup ref.

Remote updates and force-pushes are outside this reference's authorization.
Treat them as a separate operation with its own confirmation and recovery
plan.
