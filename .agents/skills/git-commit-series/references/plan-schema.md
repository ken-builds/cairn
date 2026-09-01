# CommitPlan schema

This is the single source of truth for the plan exchanged between the
planning and execution modes. The Markdown handoff is a rendering of this
structure; it must not invent fields or hide hunk ownership.

## Top-level shape

Use these fields in this order:

| Field | Type | Meaning |
| --- | --- | --- |
| schema_version | string | Version of this plan contract, currently 1. |
| mode | enum | plan, execute, or history-edit. |
| base | object | Ref and SHA against which the series is described. |
| baseline | object | Starting branch/HEAD/index/worktree snapshot. |
| ordering_basis | string | Evidence used to break ties between independent intents. |
| protected_changes | array of HunkRef | Pre-existing or explicitly protected changes kept outside the series. |
| commits | array of CommitPlanItem | Ordered candidate or actual commits. |
| excluded | array of HunkRef | Deliberately omitted changes with a reason. |
| undecided | array of HunkRef | Observed changes whose ownership or boundary needs user input. |
| open_decisions | array of Decision | Questions that prevent a safe assignment or execution. |
| residual | array of HunkRef | Task-owned changes intentionally remaining after execution. |

The ordered commits array is the proposed topological order. depends_on must
agree with that order; a dependency never points to a later item.

Use these nested fields:

~~~text
base { ref: string, sha: string }
baseline {
  head: string
  branch: string
  index_state: string
  worktree_state: string
  captured_at: string | null
}
~~~

Every observed hunk has one and only one disposition: a commit, protected,
excluded, undecided, or residual. Every undecided hunk is listed in exactly one
open Decision's affected_hunks and remains outside all commit arrays.
Execution is blocked while any blocking decision remains unresolved.

`protected` means pre-existing or explicitly preserved work; `excluded` means
outside the requested task; `undecided` means ownership or boundary needs an
answer; `residual` means task-owned work intentionally deferred beyond this
authorized series.

`basis` disambiguates mixed index/worktree views: compare staged hunks with
HEAD, worktree hunks with the index, and use the combined HEAD view to detect
overlap. `ordering_basis` records how independent DAG ties were made
deterministic.

## HunkRef

Use a hunk-level reference whenever a file contains more than one logical
change. The fields are:

~~~text
HunkRef {
  id: string                 # unique, for example H001
  source: enum               # staged | unstaged | untracked | history
  disposition: enum          # commit | protected | excluded | undecided | residual
  basis: enum                # HEAD | INDEX | WORKTREE | FILE | HISTORY
  path: string
  anchor: string             # old/new line range, symbol, or whole-file
  fingerprint: string | null # normalized patch/context hash when available
  summary: string
  classification: array      # behavior | test | refactor | formatting |
                             # generated | lockfile | debug | WIP | other
  reason: string             # required outside commit disposition
}
~~~

For a textual patch, anchor should include enough context to relocate the
hunk after nearby edits and fingerprint should identify the normalized patch
when a stable hash can be produced. For an untracked, binary, mode-change, or
rename entry, use a whole-file or operation description and identify the
verification available; fingerprint may be null.

## CommitPlanItem

Every item uses the following fields:

~~~text
CommitPlanItem {
  id: string                  # unique stable ID such as C1
  operation: string | null    # history operation when no textual hunk is owned
  subject: string             # repository-style first line
  body: string | null         # repository-style body; null when not needed
  trailers: array of string   # only required repository/task trailers
  intent: string              # one sentence, one primary purpose
  hunks: array of HunkRef     # authoritative ownership list
  files: array of string      # readable path summary, derived from hunks
  depends_on: array of string # predecessor commit IDs
  validation: array of Gate
  expected_state: string      # state after this item is applied
  rollback: string            # effect of reverting this item
  risk: string
  status: enum                # planned | validated | committed | failed |
                              # blocked; use blocked for unresolved decisions
  notes: string | null
}
~~~

subject and body follow the repository's own convention. The plan may include
a complete message in the handoff by rendering subject, body, and trailers
together. A body can be null when the repository accepts a subject-only
message.

files is a convenience view. The hunks array is authoritative for staging,
coverage, and review.

Use `validated` only when all required gates for the item passed. Use
`blocked` for an unresolved decision, baseline drift, or failure that prevents
safe continuation; use `failed` for a completed operation or gate that failed.

## Gate

~~~text
Gate {
  id: string
  command: string
  purpose: string
  expected: string
  result: enum                 # pending | passed | failed | not-run
  evidence: string | null      # output path, test name, or concise result
  reason: string | null        # required for not-run or blocked gates
}
~~~

Use one gate for each material claim. A broad suite can supplement a focused
check; it does not erase a failed focused check.

## Decision

~~~text
Decision {
  id: string
  question: string
  affected_hunks: array of string
  options: array of string
  recommended: string | null
  blocking: boolean
}
~~~

Set blocking to true when a safe plan cannot assign or execute the affected
hunks without user input.

## Invariants

Before handoff, verify all of the following:

1. Every observed hunk ID has exactly one disposition. An undecided hunk is
   accounted for through both the undecided array and an open decision, not
   assigned to a commit.
2. The undecided array and the union of all open Decisions' affected_hunks
   contain the same IDs; each undecided hunk appears in exactly one decision.
3. Every protected, excluded, residual, and undecided hunk is outside all
   commit arrays.
4. Every commit ID and hunk ID is unique.
5. Every depends_on ID exists, points backward in the ordered array, and
   produces an acyclic graph.
6. Every commit has one primary intent, a non-empty hunk list or a non-empty
   history operation, and a rollback statement.
7. Every commit has at least one validation gate, unless the repository
   demonstrably has no applicable check; in that case record a not-run gate
   and its reason.
8. A blocking open decision prevents execution. Failed, not-run, and blocked
   states are represented honestly; they are never rendered as passed or
   committed.
9. The base SHA and baseline state are sufficient to detect a changed
   worktree before execution.

## Minimal example

~~~json
{
  "schema_version": "1",
  "mode": "plan",
  "base": { "ref": "origin/main", "sha": "abc1234" },
  "ordering_basis": "Dependency edges first; stable ledger order breaks independent ties.",
  "baseline": {
    "head": "abc1234",
    "branch": "feature/search",
    "index_state": "clean",
    "worktree_state": "task-owned changes recorded",
    "captured_at": null
  },
  "protected_changes": [],
  "commits": [
    {
      "id": "C1",
      "operation": null,
      "subject": "refactor(parser): isolate token normalization",
      "body": null,
      "trailers": [],
      "intent": "Separate normalization so the later parser fix has a smaller review surface.",
      "hunks": [
        {
          "id": "H001",
          "source": "unstaged",
          "disposition": "commit",
          "basis": "WORKTREE",
          "path": "src/parser.ts",
          "anchor": "normalizeToken",
          "fingerprint": null,
          "summary": "Move behavior-preserving normalization into a helper.",
          "classification": ["refactor"],
          "reason": ""
        }
      ],
      "files": ["src/parser.ts"],
      "depends_on": [],
      "validation": [
        {
          "id": "G1",
          "command": "npm test -- parser",
          "purpose": "Confirm normalization behavior is unchanged.",
          "expected": "Relevant parser tests pass.",
          "result": "pending",
          "evidence": null,
          "reason": null
        }
      ],
      "expected_state": "Parser behavior is unchanged and the helper is available.",
      "rollback": "Revert the helper extraction without removing the later bug fix.",
      "risk": "Low; behavior should be unchanged.",
      "status": "planned",
      "notes": null
    }
  ],
  "excluded": [],
  "undecided": [],
  "open_decisions": [],
  "residual": []
}
~~~

Use stable IDs throughout one handoff. If the baseline changes, create a new
plan version and reassign IDs rather than silently reusing stale ownership.
