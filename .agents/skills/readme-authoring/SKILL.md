---
name: readme-authoring
description: Write, audit, and revise repository-level README files from verified project facts, adapting the structure for libraries, CLIs, applications, services, templates, and monorepos; use for README work, not general documentation or code implementation.
---

# README Authoring

Use this skill when a repository needs a new README, a factual audit, or a focused
revision of an existing README. The deliverable is a reader-oriented README draft or
approved in-place edit whose actionable claims are traceable to the repository or a
dated authoritative source.

## Boundary and operating contract

This skill covers the repository root README and deliberately selected package or
component READMEs. It covers positioning, prerequisites, installation, the first
successful use, configuration, development, and the contribution/support/security
entry points that a reader needs. It does not write general API reference, architecture
records, release notes, code, CI, or deployment configuration. Hand those requests to
the relevant documentation, architecture, or implementation skill.

Start in `design` mode. Read-only inspection may produce an audit, a fact ledger, a
section outline, and a Markdown preview in the response. Move to `record` only after
the user approves the preview and exact target path. Move to `probe` only after the
user authorizes execution in a disposable directory. Keep the repository and external
systems unchanged in `design`; a missing prerequisite is `unknown`, `not-run`, or
`blocked`, never a claimed pass.

An existing README is the baseline. Preserve accurate project language, useful links,
and stable anchors; make an incremental revision unless the baseline is materially
misleading or unusable. If more than one README could be the target, surface the
choice before writing.

## Stable vocabulary and states

Keep these leading words stable:

- **baseline** — the current README, repository state, and protected changes.
- **audience** — the primary reader and the job they need to complete.
- **archetype** — library, CLI, application, service, template, or monorepo shape.
- **Map** — the evidence-backed route from entry point to a reader's first success.
- **fact ledger** — each actionable claim, its source, and its verification state.
- **spine** — the smallest useful section order for this audience and archetype.
- **success path** — the shortest copyable path from prerequisites to a visible result.
- **sensor** — a static check that catches stale structure, links, or repository references.
- **probe** — a bounded sandbox run of the success path.
- **handoff** — the concise audit, preview, validation, and authorization summary.
- **drift** — a later README claim that no longer matches the repository.

Use these states exactly for facts, checks, and probes: `confirmed`, `inferred`,
`unknown`, `not-run`, and `blocked`.

## Conditional references

Read only the reference reached by the current branch:

- Read [readme-contract.md](references/readme-contract.md) before building the fact
  ledger, drafting a preview, or recording a change.
- Read the matching section of [archetype-profiles.md](references/archetype-profiles.md)
  after identifying the repository archetype.
- Read [verification.md](references/verification.md) before running the sensor or a
  `probe`, especially when commands, network access, credentials, or cleanup are involved.

## Workflow

### 1. Establish the baseline

1. Locate the repository root and read repository-local instructions, contribution
   guidance, manifests/lockfiles, scripts, CI, examples, licenses, security policy,
   and existing README files. Capture branch/worktree status and protected changes.
2. Identify the requested README path, current language, nearby documentation, and any
   constraints supplied by the user. Keep an explicit list of paths in scope and out of
   scope.

**Done when:** the target path, protected state, rule sources, existing README content,
and missing prerequisites are recorded without changing the repository.

### 2. Identify the audience and archetype

1. Name the primary audience (for example, evaluator, end user, integrator, contributor,
   or operator) and the one job that should succeed first.
2. Classify the repository as one or more of `library`, `cli`, `application`, `service`,
   `template`, or `monorepo` using actual files and scripts. If signals conflict, keep the
   ambiguity visible and choose the narrowest safe profile for the draft.
3. Choose the README language from existing repository language and audience evidence;
   preserve established product and API terms.

**Done when:** one audience, archetype profile, language strategy, and first-success
outcome are explicit and evidence-backed.

### 3. Build the fact ledger and Map

1. Trace the success path from prerequisites through installation and the first observable
   result. Verify commands against manifests, package scripts, entry points, Make targets,
   container files, examples, and CI rather than inventing them from convention.
2. Record each claim with source path or official URL, version/date when dynamic, and one
   of the allowed states. Separate repository fact, inference, user-provided fact, and
   unknown. Mark secrets, private endpoints, and environment-specific values for removal
   or safe substitution.
3. Account for public entry points, configuration names, supported platforms, examples,
   test/development commands, contribution route, license, and support/security contact.

**Done when:** every actionable sentence planned for the README has a fact-ledger entry,
and every unknown has an owner or a concrete next check.

### 4. Design the spine

1. Start with the smallest spine: project identity and value, prerequisites, installation,
   success path, usage/configuration, development/testing, and only the contribution,
   support, security, license, or links sections that the repository supports.
2. Apply the selected archetype profile. Keep a section only when it answers a reader job;
   link to deeper documentation instead of duplicating it. Preserve valid existing anchors
   where practical.
3. Order instructions so a fresh reader can copy the success path without jumping across
   unrelated prose. Put assumptions and platform forks next to the command they affect.

**Done when:** the section order, inclusion rationale, link targets, and platform forks are
settled, with no section relying on an unowned claim.

### 5. Draft or revise incrementally

1. Write a concise opening that says what the project is, who it is for, and what result it
   provides. Use the repository's canonical names and language.
2. Make installation and success-path snippets copyable: show prerequisites, working
   directory, required environment/configuration, expected output or verification, and
   cleanup where relevant.
3. For an existing README, retain accurate material and edit only stale, missing, or
   misleading portions. Show a focused diff/preview in the response; do not create a
   separate audit report unless the user requests one.

**Done when:** the draft contains no unresolved placeholders or unsupported claims, the
success path is complete on paper, and the preview identifies every material change.

### 6. Run sensors and classify evidence

1. Run `scripts/validate_readme.py` against the target README with `--profile auto` (or
   the chosen explicit profile). Treat structural failures as blockers to recording.
2. Check local links, code fences, referenced paths, command/script names, package names,
   placeholder markers, and accidental credentials. Use `--strict` when explicit
   repository references or install-package consistency needs checking. Static checks do
   not prove a command works; keep that distinction in the handoff.
3. For dynamic versions, external services, badges, or installation instructions, consult
   official sources only when the fact can change the reader's action; record URL and access
   date, and label unavailable research `not-run` or `blocked`.

**Done when:** the sensor output is passing or every failure has a documented disposition,
and dynamic claims have a source or an explicit verification state.

### 7. Run the optional probe

Read [verification.md](references/verification.md) first. After explicit `probe`
authorization, copy the minimum project inputs to a disposable temporary directory,
pin the intended runtime, run only the named success path with a timeout, and remove
the temporary state. Never paste real credentials or mutate production services.

**Done when:** the success path is `confirmed` by a reproducible sandbox result, or the
exact command, prerequisite, limitation, and next action are recorded as `not-run` or
`blocked`.

### 8. Record only an approved edit and hand off

1. Before writing, recheck the baseline and confirm that the approval names the exact
   README path and preview. If the baseline drifted, stop and refresh the audit.
2. Apply only the approved README change. Inspect the final diff with `git diff --check`,
   rerun the sensor, and leave unrelated files, generated output, and protected changes
   untouched.
3. Return the handoff: target path, audience/archetype/language, source summary, changed
   sections, sensor results, probe state, unresolved facts, and any follow-up owner.

**Done when:** the final README matches the approved preview, validation evidence is
attached, and a fresh agent can explain what remains without reconstructing hidden work.

## Response handoff

End with a compact handoff containing: baseline and target path; audience, archetype, and
language; success path; changed sections; fact-ledger/source status; sensor command and
result; probe command and state; unresolved questions with owners; and the next required
authorization. The README is the long-lived artifact; the response is its audit index.
