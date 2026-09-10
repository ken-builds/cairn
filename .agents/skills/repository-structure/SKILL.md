---
name: repository-structure
description: Component boundaries and repository layout. Use before adding or splitting components, moving public entrypoints, changing allowed dependencies, or expanding a directory with growth, cohesion, or local-context signals.
---

# Repository Structure

Align the physical tree with component responsibilities, visibility, and dependency rules.
A directory may be a container rather than a boundary. Keep a cohesive flat layout as a
valid candidate. Apply this workflow across languages and build systems.

## Scope and authority

Reuse the user's authorized scope. `design` is read-only investigation; `probe` is bounded
experimentation; `record` writes reviews/context; `migrate` moves agreed paths and updates
references. These are capabilities, not mandatory successive approval prompts. Confirm a
migration's exact paths and effects within the authorized scope before moving. Preserve
existing changes and separate unrelated behavior changes from path moves.

Public contract, runtime, data, or deployment decisions belong to `architecture-design`
when installed. Pass discovered boundaries and questions; retain pending decisions if it
is unavailable. User-invoked `git-commit-series` is an optional next step the user can
request, not an automatic invocation.

## 1. Recover the boundary and baseline

Inspect applicable agent instructions, the nearest component README, manifests/build
markers, ownership sources, and linked records. Capture revision, protected changes,
target roots, outcome, and non-goals. Verify prose against executable sources.

Build the **Map** from scoped paths, entrypoints, configured wiring, and available native
dependency reports. Record purpose, owner or owned unknown, consumers, lifecycle, visibility,
and allowed edges. Retain the search/report scope and unresolved edges.

**Done when:** each discovered path belongs to a component or explicit container, each
public entrypoint has an owner, and discovered cross-boundary edges have evidence or a
next check. Unavailable dependency information remains `unknown`.

## 2. Measure and select the branch

For a growth, cohesion, or file-count question, read
[signals-and-thresholds.md](references/signals-and-thresholds.md). Count direct production
files separately from recursive descendants, tests, generated/vendor files, and tooling.
Use native reports or `scripts/inventory_structure.py`; state scanned roots, exclusions,
and role uncertainty. Prefer native graph/history tools for dependencies and co-change.
File counts trigger review rather than selecting a layout.

- For new/split components or changed dependency/visibility boundaries, read
  [component-design.md](references/component-design.md) before proposing paths.
- For a new, missing, or changed boundary README, read
  [component-readme-contract.md](references/component-readme-contract.md) before drafting.
  Use `readme-authoring` when installed for prose/link verification; the local contract
  remains sufficient to identify purpose, constraints, and sources without it.
- For external precedent, read [industry-patterns.md](references/industry-patterns.md)
  and verify the particular mechanism being used.

**Done when:** each observed signal has a sourced measurement or semantic finding and a
disposition: retain, document, review, migrate, or waive. Each discovered boundary has a
local-context disposition; ordinary containers need no documentation by quota.

## 3. Compare structures

Keep **C0** as the current tree or smallest change. Compare capability grouping, independent
package/build/ownership boundaries, or local dependency layers only when findings warrant
them. Use the component-design branch to identify contract ownership and substitution impact.
Compare cohesion, navigation, enforcement, compatibility, migration cost, and expected change.

**Done when:** the chosen layout addresses a named finding, affected abstractions have
consumer/implementation ownership, and changed allowed edges are explicit. Explain why
retained flat groups or new nesting fit the evidence and what would reopen the decision.

## 4. Record and apply the selected increment

Before writing a review/policy, read [structure-contract.md](references/structure-contract.md).
Reuse a Brief or ADR where possible. A read-only review can stay in the response. At each
authorized increment, keep a short checkpoint of changed boundaries, public paths,
assumptions, and checks in existing task notes or a record.

For path moves, read [migration-playbook.md](references/migration-playbook.md). Apply agreed
paths, references, build/ownership metadata, and local context together. When public
declarations or failure/lifecycle/compatibility behavior changes, use the corresponding
`implementation-rationale` branch during implementation if installed. Otherwise preserve
the affected contract/rationale at its owning declaration or test and expose pending review.

**Done when:** implemented paths and changed edges match the selected increment, or
differences have reopened the decision. Each newly found boundary receives the same
assessment; an earlier accepted review covers only its recorded scope.

## 5. Verify the actual coverage

Read [sensors-and-adapters.md](references/sensors-and-adapters.md) when selecting or changing
checks. Compare the final tree and allowed edges with the Map. Verify each required check
is reached by the owning gate and selects intended targets. Report accepted, rejected,
skipped, and unsupported targets separately. For a new/materially changed critical gate,
use a valid fixture and controlled violation to demonstrate detection in isolation.

**Done when:** each invariant relied on by the increment has evidence of coverage and an
actual result, or an explicit gap with owner/next check. Document-format success, inventory
measurements, graph enforcement, and semantic review remain distinct claims.

Finish with the selected structure, reasons, actual verification scope, record links, and
remaining decisions. The Map/configuration owns the detail; the response is a compact index.
