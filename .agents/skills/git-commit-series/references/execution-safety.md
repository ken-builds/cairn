# Controlled execution

Read this reference only after the user has explicitly authorized the named
commit scope. It turns a handoff into one-commit-at-a-time Git operations while
preserving the baseline and protected changes.

## Preflight gate

1. Re-read the plan and capture the current HEAD, branch, index patch,
   worktree patch, and untracked paths.
2. Compare those values with the plan baseline. A changed HEAD, changed
   task-owned hunk, new overlap, or changed repository rule starts a new plan.
3. Enumerate protected and residual paths. If a protected staged hunk would be
   included by the next commit, isolate it with a temporary index or ask the
   user to resolve the overlap before continuing.
4. Confirm the authorization covers the exact commit IDs and whether local
   fixups or history rewriting are allowed.

When staged protected changes share a path with task hunks, first normalize the
two views against the same HEAD: inspect `git diff HEAD -- <path>`, treat
`git diff --cached` as the HEAD→index delta, and treat `git diff` as the
index→worktree delta. Keep those bases distinct in the ledger. Prefer asking
for a clean index. If the user authorizes a temporary index, save the original
index path and object,
set `GIT_INDEX_FILE` only for the isolated staging/commit, and restore the
original index after the commit. Reconcile it against the new HEAD by checking
`git diff HEAD --cached`; re-stage protected hunks if policy permits, or stop
when the original index cannot be represented safely after HEAD advances.

Useful read-only checks:

~~~sh
git status --short --branch
git rev-parse HEAD
git diff --cached --binary
git diff --binary
git ls-files --others --exclude-standard
~~~

**Preflight is complete** when the current snapshot matches the plan or a
revised plan has been accepted, and the protected scope has an explicit
preservation strategy.

## Staging gate

For each commit in topological order:

1. Select only its listed paths or hunks. Use path-scoped staging for a wholly
   owned file and patch-level staging for a mixed file. A path-scoped add is
   unsafe when protected and task hunks share that path.
2. Inspect the staged patch and compare every hunk with the plan's ownership
   IDs.
3. Run the integrity checks before creating the commit.

~~~sh
git diff --cached --name-status
git diff --cached --check
git diff --cached --binary
~~~

The cached diff is the authority for what will be committed. A broad
whole-tree add is not a substitute for this comparison. A mismatch pauses the
loop and returns to the ledger; it does not get “fixed” by guessing.

When later, unstaged task changes could affect a test, validate in an isolated
temporary worktree or clearly record the contamination risk. Keep the real
worktree and index available for recovery.

**Staging is complete** when the cached patch contains exactly one planned
commit and no protected or residual hunk.

## Commit and per-item gate

1. Run the candidate's focused validation, then any repository-required gate.
2. Record command, result, and evidence in the plan.
3. Create exactly one commit using the approved subject, body, and trailers.
4. Record the resulting full hash and inspect the new commit.

~~~sh
git commit
git show --stat --oneline --decorate HEAD
git show --check HEAD
git status --short --branch
~~~

The commit hook or signing policy is part of the repository source of truth.
Let it run unless the user explicitly authorizes a documented override, and
record any hook-generated change or failure.

**Per-item execution is complete** when the hash, validation result, staged
scope, and post-commit status are attached to that plan item.

## Failure handling

- A staging mismatch returns to the hunk ledger and may require a new plan.
- A failed validation leaves the candidate uncommitted. Diagnose, repair, or
  mark the item blocked; continue only after the plan and authorization cover
  the repair.
- An unavailable executable or test entry point is `not-run` with the missing
  prerequisite recorded; a command that starts and exits unsuccessfully is
  `failed`.
- A hook failure is a failed gate until the repository-required cause is
  addressed.
- A conflict or interrupted operation pauses the series. Use the operation's
  native abort path only when the user authorized it, then recheck the
  baseline.
- A local fixup commit is appropriate for an implementation correction that
  belongs to an earlier intent. Use fixup/autosquash only when local history
  cleanup is authorized, and report the rewrite.

## Protected index and worktree changes

Keep pre-existing staged changes out of task commits. Prefer asking for a clean
index when direct staging would mix them. If the user authorizes an explicitly
created temporary index initialized from the planned base, save the original
index path and object, stage only task hunks there with patch selection (never a
whole-path add for a mixed path), and commit from that isolated index. Restore
the original index after the commit, compare `git diff HEAD --cached` with the
saved protected patch, and re-stage protected hunks only with explicit
permission. If the original index cannot be reconciled after HEAD advances,
stop and request a clean boundary rather than resetting the user's index.

Keep protected unstaged and untracked paths untouched. Avoid stash, clean,
reset, checkout, or overwrite operations unless each exact target and effect
has been authorized.

## Final audit

After the last authorized item:

~~~sh
git log --oneline --decorate <base>..HEAD
git diff --stat <base>..HEAD
git status --short --branch
~~~

Use git range-diff when the series was amended or autosquashed. Compare the
actual diff with the plan's hunk ledger, verify protected and residual paths,
and report every hash, gate result, deviation, and uncommitted change.

**Execution is complete** when the authorized series is auditable and the
remaining worktree/index state is explained path by path.
