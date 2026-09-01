---
name: git-commit-series
description: Plan and, after explicit approval, execute a reviewable Git commit/patch series from mixed changes. Use when explicitly invoked to organize a large diff into logical, dependency-ordered commits.
disable-model-invocation: true
---

# Git Commit Series

Use this skill after the user explicitly invokes it to turn a mixed or large
change into a coherent commit series, or to reorganize local commits. It is a
planning and controlled-execution workflow, not a generic Git tutorial or a
single commit-message writer.

## Modes and authorization

Choose one mode before reading the diff:

- **plan** (default): analyze the current worktree and produce a CommitPlan.
- **execute**: apply an approved plan one commit at a time.
- **history-edit**: split, reorder, squash, or otherwise rewrite existing local
  commits. Read references/history-surgery.md only for this mode.

Planning always comes first. Execution authorization must identify this plan
and either exact commit IDs or the complete resolved series; it never includes
undecided items. A request to organize, review, or propose commits
authorizes analysis only. Pushes, force-pushes, and changes outside the named
scope need separate confirmation.
If a baseline drift causes a revised plan, obtain authorization again for the
revised plan and exact IDs. If no matching handoff exists, stay in plan mode
even when the user asks to execute immediately.

In **plan** mode, keep Git refs, the index, and tracked files unchanged. If the
worktree or task scope changes after a plan, establish a new baseline before
executing it.

## Invariants

Keep these leading words visible while working:

- **baseline** — the starting HEAD, index, worktree, and protected changes.
- **hunk ledger** — the complete accounting of every observed diff hunk.
- **intent** — the one logical reason for a commit.
- **DAG** — dependency edges between intents, later topologically ordered as a
  **series**.
- **green gate** — the checks that make a candidate commit understandable and
  verifiable.
- **handoff** — the stable plan another agent can execute without guessing.
- **residual** — changes intentionally left outside the series.

The series is correct only when every observed hunk has exactly one disposition,
every commit has one primary intent, dependencies are acyclic, protected
changes stay protected, and each public commit has an explicit validation
state. The smallest useful unit is a complete logical change, not a file,
directory, or line-count quota.

## Workflow

### 1. Establish the baseline

1. Locate the repository root, current branch or detached HEAD, intended base
   ref, and any merge/rebase policy. If no explicit base is supplied and no
   upstream is available, use the current HEAD only as a clearly recorded
   assumption; if more than one base is plausible, create a blocking decision.
   If the directory is not a Git repository, stop with a bounded explanation;
   if the repository has no commit yet, require an explicit base or report that
   a commit series cannot be anchored to a parent.
2. Read repository-local instructions and sources of truth in this order:
   AGENTS.md/CLAUDE.md, contribution docs, commit hooks or lint
   configuration, package/build scripts, CI definitions, and recent history.
3. Capture one read-only snapshot of branch, HEAD, index status, worktree
   status, staged and unstaged patches, untracked paths, and the relevant
   base..HEAD history. If there are no task-owned changes, report an empty
   series and the protected/residual state instead of inventing a commit.
   Normalize mixed staged and unstaged changes against their correct parents,
   then use the combined HEAD view to detect overlap; do not treat two diff
   views as one hunk stream.
4. Classify changes as task-owned candidates, protected, excluded, undecided,
   or residual. A task-owned candidate receives the `commit` disposition only
   after it is assigned to a series item. Use an explicit pre-task snapshot or
   the conversation as ownership evidence.
   If the base or ownership boundary has more than one plausible interpretation,
   place the affected changes in the undecided bucket and create a blocking
   decision; do not silently produce an executable plan.
   Keep the five dispositions disjoint. An undecided hunk belongs in the
   undecided ledger bucket and blocks execution until resolved.

**Done when:** the rule sources, base SHA, baseline state, and a disjoint
disposition for every visible hunk are recorded; blocking ambiguity is surfaced.

### 2. Build the hunk ledger

Read [boundary-rules.md](references/boundary-rules.md) when assigning ownership.
Inspect the complete diff, enabling rename detection when useful. Include
untracked files, renames, binary files, generated artifacts, and lockfiles.
Read untracked content explicitly (the default tracked-file diff omits it),
and represent an untracked file as a whole-file hunk when finer ownership is
impossible.

For each hunk, record its stable ID, path, old/new line anchor, short context
or patch fingerprint, concise summary, intent, behavior impact, direct tests,
dependencies, validation, rollback effect, and classifications such as
formatting, generated, lockfile, debug, or WIP. Merge coupled hunks when
separating them would create an unreviewable or unbuildable state.

**Done when:** every observed hunk appears exactly once across candidate
groups, protected, excluded, undecided, or residual buckets.

### 3. Form atomic intents and the dependency DAG

Cluster by intent, coupling, review boundary, and rollback boundary. Keep
behavior and its directly coupled tests together. Give independent mechanical
refactors, formatting, documentation, dependency maintenance, and unrelated
cleanup their own intent when they can stand alone. Keep a cross-file change
together when it expresses one logical change. Follow real migration
dependencies (for example, expand/compatibility layer → callers → contract or
cleanup), and follow the repository's rules for lockfiles and generated output.

Do not let a message type such as feat, fix, or refactor decide the boundary.
Prefer a green series: each public point should build and pass the smallest
relevant checks. A necessarily red intermediate state belongs in local fixup
work, or is called out as an explicit repository-approved exception.

Create one directed edge for each required predecessor, detect cycles, and
topologically sort the result into C1…Cn. Read the boundary reference again
for migration, generated-file, lockfile, or inseparable-hunk cases.

**Done when:** the candidate groups cover the ledger without overlap, each
group has one sentence-level intent, the DAG has no cycle, and the sorted
series is minimal but complete.

### 4. Apply the green gate

Discover validation commands from the repository rather than copying a generic
command list. In plan mode, run only known read-only checks. Materialize a
candidate with a disposable filesystem copy before a build or test that could
create tracked or untracked artifacts; keep the source repository unchanged. A
`git worktree add` may change repository metadata, so use it only with explicit
permission. If the executable or test entry point is unavailable, mark the gate
not-run and name the missing prerequisite; reserve failed for a command that
actually ran and failed.
Select a focused check for each candidate, add broader checks where policy
requires them, and include git diff --check when applicable. Mark every check
pending, passed, failed, or not-run; an unrun check is never a pass.

Check that each candidate can be reviewed and reverted on its own, that
debug/WIP material is accounted for, and that the proposed message follows the
repository's actual convention. Use a Conventional Commits shape only as a
fallback when no local convention exists.

**Done when:** every candidate has a command, purpose, expected result, current
validation state, and a recorded explanation for anything not run.

### 5. Produce the handoff

Read [plan-schema.md](references/plan-schema.md) for the authoritative fields
and [output-template.md](references/output-template.md) for the presentation
contract. Output the schema version, base and baseline, protected, excluded,
undecided, and residual changes, the dependency order, and each commit's
operation, subject/body, intent, exact hunk ownership, dependencies,
validation gates, risk, rollback, and status. List open decisions instead of
silently choosing across an unresolved boundary.

In plan mode, stop after this handoff. The handoff is complete when another
agent can stage exactly one planned commit at a time without inferring where a
hunk belongs.

### 6. Execute only an approved handoff

After explicit authorization, read
[execution-safety.md](references/execution-safety.md). Recheck the baseline,
confirm the authorization covers the exact resolved IDs, then use path- or
hunk-scoped staging, inspect the cached diff, run that commit's green gate, and
create exactly one commit before moving to the next.
If the actual diff no longer matches the plan, pause and re-plan. For
history-edit mode, also read [history-surgery.md](references/history-surgery.md).

**Done when:** every authorized plan item has one recorded commit result and no
protected change was staged or rewritten.

### 7. Audit the result

Compare the actual series with the handoff using commit log inspection,
base..HEAD diff review, and range-diff when history was rewritten. Recheck
status, protected changes, residual paths, and every validation result. Report
hashes and deviations; distinguish passed, failed, not-run, and blocked.

**Done when:** the final report accounts for every planned item, every
residual change, and every mutation made.

## Conditional references

- Read references/boundary-rules.md during hunk classification and whenever a
  change mixes behavior, tests, refactoring, migration, generated output,
  lockfiles, or WIP.
- Read references/plan-schema.md and references/output-template.md before
  producing the handoff.
- Read references/execution-safety.md only after execution is authorized.
- Read references/history-surgery.md only when existing commit history will be
  rewritten.
