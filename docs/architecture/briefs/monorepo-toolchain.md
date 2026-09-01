# Foundation Brief: monorepo-toolchain

Status: draft
Date: 2026-09-01
Owner: Cairn maintainers

## Objective

Provide a reproducible local foundation for a pnpm monorepo of private packages. A new contributor should be able to install the declared toolchain, run one aggregate quality gate, and receive deterministic feedback before a commit is created.

## Non-goals

Product behavior, deployment infrastructure, CI, package publishing, changelog automation, independent package release ordering, and a production TypeScript/build pipeline are deferred.

## Mandate and baseline

The supplied mandate requires mise for development environment management and executable file tasks, pre-commit and Cocogitto for local commit checks, pnpm for an internal workspace, and Biome, Knip, and Oxlint as quality gates. The repository is an empty shell with a short README, two existing Conventional Commits, no tags, and no protected application code. The target environment is a POSIX developer workstation. Cairn maintainers own the root configuration; package owners own package manifests and source. Record authorization is active for this initialization.

## Constraints and assumptions

| ID | Constraint or assumption | Impact if false | Validation/owner | State |
| --- | --- | --- | --- | --- |
| A1 | Node 22 is the supported LTS line and must satisfy pnpm and the Node-based analyzers. | Runtime and lockfile compatibility may change. | Maintainers check mise and registry compatibility before a runtime upgrade. | inferred |
| A2 | The initial task scripts target macOS/Linux POSIX shells. | Windows needs paired PowerShell tasks and a different pre-commit distribution. | Platform owner reviews after the first non-POSIX contributor. | inferred |
| A3 | `@cairn/*` is the internal package namespace. | Package names and future publishing scope must be migrated. | Repository owner confirms before the first publishable package. | inferred |
| A4 | The root `pnpm-workspace.yaml` is the only workspace discovery source. | Tooling may discover a divergent package set. | Package owners update the workspace contract in one ADR. | confirmed |
| A5 | Pre-commit owns both `pre-commit` and `commit-msg` hooks. | A later installer could overwrite one stage. | Maintainers inspect hook ownership during setup changes. | confirmed |
| A6 | Oxlint is dedicated to the classic complexity rule with a maximum of 20. | Existing code may require a migration or a stricter/looser baseline. | Maintainers review complexity reports at the next package increment. | confirmed |
| A7 | No CI or release automation is required for this foundation. | A remote gate and release policy must be designed separately. | Product owner opens a follow-up architecture decision. | confirmed |

## Context Map

Contributors invoke `mise run setup`, `mise run check`, and `mise run format`. Mise supplies the pinned Node, pnpm, Python, pre-commit, and Cocogitto executables and discovers scripts under `.mise/tasks`. Pnpm reads `pnpm-workspace.yaml`, installs the root quality tools, and runs package scripts across `packages/*`. The pre-commit framework invokes the aggregate check during `pre-commit` and invokes `verify-commit` during `commit-msg`. The verify task passes the Git message file to Cocogitto. The npm registry, PyPI/aqua release assets, and Git repository are external trust boundaries; no production runtime or business data is in scope. Package manifests own package metadata, source files own implementation, and the root lockfile owns the resolved JavaScript dependency graph.

## Glossary

| Term | Scope | Canonical meaning | Source | Aliases/relations |
| --- | --- | --- | --- | --- |
| Workspace | Repository | The pnpm-managed set of the root project and packages matched by `packages/*`. | `pnpm-workspace.yaml` | monorepo |
| Internal package | Package boundary | A private package under `packages/*` that can be consumed through a `workspace:` dependency. | package manifests | workspace package |
| File task | Development tooling | An executable script discovered by mise from `.mise/tasks`. | `mise.toml` and `.mise/tasks` | task |
| Quality gate | Commit boundary | A read-only command whose non-zero exit status blocks the local commit. | `package.json` and `.pre-commit-config.yaml` | local gate |
| Complexity | Source quality | Classic cyclomatic complexity measured by Oxlint's ESLint-compatible `complexity` rule. | `.oxlintrc.json` | McCabe complexity |
| Commit message | Git boundary | The text file checked by Cocogitto during the `commit-msg` stage. | `.pre-commit-config.yaml` | Conventional Commit |

## Drivers and scenarios

| ID | Stimulus | Context | Response | Metric | Threshold | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | A contributor clones the repository on a supported workstation. | No project tools or Node shims are active. | `mise run setup` installs the declared environment, completes a frozen pnpm install, and installs both hook types. | Bootstrap command status | Exit status 0 with no manual global Node/pre-commit installation. | P0 |
| D2 | A staged source or config change violates formatting or a Biome recommended rule. | `pre-commit` stage runs from the repository root. | The aggregate gate reports the violation and blocks the commit without modifying files. | Gate exit status | Non-zero before commit creation; clean tree remains unchanged. | P0 |
| D3 | A package contains a function whose classic complexity exceeds the configured limit. | Oxlint scans `packages`. | Oxlint reports an error and blocks the commit. | Complexity score | Any score greater than 20 returns non-zero. | P0 |
| D4 | A contributor writes a non-Conventional commit message. | `commit-msg` stage receives one message file. | The verify task delegates to Cocogitto and rejects the message. | Verification status | Invalid message returns non-zero; a valid `type: description` message returns 0. | P0 |
| D5 | A package or root script becomes disconnected from the workspace graph. | Knip analyzes the pnpm workspace. | Knip reports the unused, unresolved, or unlisted item. | Knip status | `knip --no-progress --treat-config-hints-as-errors` returns 0 only for a clean graph. | P1 |

## Candidates

| ID | Option | Fit | Trade-offs | Reversibility | State |
| --- | --- | --- | --- | --- | --- |
| C0 | Hybrid toolchain: mise for runtimes and native commit tools, pnpm devDependencies for JS analyzers, pre-commit as hook owner. | Satisfies all supplied tool choices while keeping package tooling visible to pnpm and Knip. | Requires both mise and pnpm bootstrap paths. | Each tool can move to another backend or package boundary without changing package contracts. | inferred |
| C1 | Install every tool through mise. | One environment manifest and no JS devDependencies. | Knip cannot see shell-only tool usage as package binaries; hook PATH and platform backends become more fragile. | Tool source can be changed, but package lock and editor schemas become less local. | inferred |
| C2 | Use an npm hook manager and commit-message package in place of the native tools. | Familiar Node-only workflow. | Conflicts with the explicit pre-commit/Cocogitto preference and adds another hook owner. | Removal is easy, but scripts and hook files would need replacement. | rejected |

## Foundation Blueprint

| Concern | Target shape | Owner | Evidence/state |
| --- | --- | --- | --- |
| Boundaries | Root tooling owns orchestration; each `packages/*` directory owns one private package; no application or deployable service boundary exists yet. | Architecture owner | inferred |
| Dependency direction | Package source may depend on declared workspace packages through `workspace:`; tooling scripts depend on package manifests, never the reverse. | Package owners | confirmed |
| Interfaces/contracts | Root scripts expose `format`, `format:check`, `lint`, `test`, `knip`, and `check`; mise tasks expose `setup`, `check`, `format`, and `verify-commit`; hook stages pass only the contractually required inputs. | Tooling owner | confirmed |
| Data ownership | `package.json` owns package metadata, `pnpm-workspace.yaml` owns discovery, and `pnpm-lock.yaml` owns resolved npm dependencies. There is no business datastore. | Package owners | confirmed |
| Runtime/deployment | Local POSIX execution uses mise-managed Node 22, Python 3.12.14, pnpm 11.25.0, and native commit tools. There is no deployment topology. | Platform owner | inferred |
| Security/trust | Tool downloads come from declared aqua/npm registries; secrets and local environment files are ignored; hooks run against the contributor's working tree and can still be bypassed with normal Git flags. | Maintainers | inferred |
| Observability | Gate output is the local signal; failures identify the responsible command. No runtime logs, metrics, or alerts are required before a service boundary exists. | Tooling owner | inferred |
| Delivery/release | A local setup task and a frozen pnpm lockfile are the only release surfaces. CI, publishing, changelog, and package bump automation are deferred. | Maintainers | confirmed |
| Cost/capacity | Tool installation and gate runtime are bounded by local developer resources; no hosted capacity or spend is introduced. | Maintainers | inferred |

## Evidence

| ID | Claim | Source | Version/commit | Accessed/measured | State | Applicability |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | mise discovers executable scripts from `.mise/tasks` and supports `#MISE` metadata. | https://mise.jdx.dev/tasks/file-tasks.html | mise 2026.8.14 docs | 2026-09-01 | confirmed | Project task layout |
| E2 | A pnpm workspace is declared with `pnpm-workspace.yaml` and package globs. | https://pnpm.io/workspaces | pnpm docs 11/12 | 2026-09-01 | confirmed | Package discovery |
| E3 | pre-commit local hooks can target named stages and use system executables through `unsupported`. | https://pre-commit.com/ | pre-commit 4.6.2 docs | 2026-09-01 | confirmed | Hook orchestration |
| E4 | Cocogitto validates a message file with `cog verify --file`. | https://docs.cocogitto.io/guide/git_hooks.html | Cocogitto 7.0.0 docs | 2026-09-01 | confirmed | Commit-message check |
| E5 | Biome supports `files.includes`, VCS ignore integration, formatter settings, and recommended rules. | https://biomejs.dev/reference/configuration/ | Biome 2.5.11 docs | 2026-09-01 | confirmed | Formatting and lint |
| E6 | Knip reads pnpm workspace packages and supports workspace-aware dependency analysis. | https://knip.dev/features/monorepos-and-workspaces | Knip 6.34.0 docs | 2026-09-01 | confirmed | Dependency graph |
| E7 | Oxlint's ESLint-compatible complexity rule accepts `max` and `variant` options. | https://oxc.rs/docs/guide/usage/linter/rules/eslint/complexity | Oxlint 1.80.0 docs | 2026-09-01 | confirmed | Function complexity |
| E8 | The chosen npm tool versions satisfy the Node 22 engine constraint. | https://www.npmjs.com/package/pnpm/v/11.25.0 and https://www.npmjs.com/package/knip/v/6.34.0 | pnpm 11.25.0; Knip 6.34.0 | 2026-09-01 | confirmed | Runtime baseline |

## Probes

| ID | Question | Hypothesis | Workload/input | Environment | Baseline | Method/budget | Threshold | Result | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Does the fresh checkout bootstrap and pass all local gates with the selected pins? | C0 completes setup and checks without a global Node or npm-tool dependency. | This repository, one private package, one Node test, one valid commit message. | macOS arm64, mise 2026.8.14, pinned tools. | No project manifest or lockfile existed before initialization. | Run `mise run setup`, then all verification commands once; no production services. | Setup and every gate exit 0. | Pending completion in the implementation verification pass. | not-run |
| P2 | Does Oxlint reject a function above the complexity limit while accepting the starter package? | The explicit `complexity` rule is active and the starter remains below 20. | One temporary function with score 21 and the committed example package. | Oxlint 1.80.0 with `.oxlintrc.json`. | No JavaScript source existed before initialization. | Run the package gate and a disposable negative fixture; preserve no fixture in the repository. | Score 21 fails; starter source passes. | Pending completion in the implementation verification pass. | not-run |

## Decision

Selected candidate: C0

Rationale: The hybrid foundation keeps runtime and native commit tools reproducible through mise while keeping JavaScript quality dependencies visible to pnpm, its lockfile, and Knip.

Sensitivity points: Windows support, a requirement for independent package releases, a stable TypeScript/build boundary, or a measured need for CI would change the selected shape. A sustained complexity failure rate would change the threshold or require a migration increment.

ADR links: [ADR-0001](../decisions/ADR-0001-toolchain-ownership.md), [ADR-0002](../decisions/ADR-0002-local-quality-gates.md)

Deferred/rejected: All-mise installation, npm hook managers, Cogo monorepo resolver and bump order, CI workflows, publishing, and production deployment are deferred or rejected for this foundation.

## Bootstrap plan and gates

| Gate | Entry | Deliverables | Exit criterion | Owner | State |
| --- | --- | --- | --- | --- | --- |
| G0 Mandate | Supplied tool and workflow requirements exist. | Objective, users, constraints, non-goals, and assumptions. | A reader can state the local success boundary and all material constraints. | Cairn maintainers | confirmed |
| G1 Context and boundaries | G0 is recorded. | Context Map, Glossary, package/tool ownership, and prioritized scenarios. | Every important boundary has an owner and contract direction. | Architecture owner | confirmed |
| G2 Blueprint and decisions | G1 is recorded. | Candidate matrix, selected hybrid blueprint, and ADR links. | Hard drivers have thresholds and sensitivity points. | Architecture owner | confirmed |
| G3 Walking skeleton | G2 is recorded and implementation is authorized. | Setup, package test, quality gate, commit-message path, and negative checks. | One end-to-end local stimulus reaches an observable acceptance result. | Tooling owner | not-run |
| G4 Handoff | G3 checks are complete or explicitly classified. | Validated records, ordered tasks, sensors, and open-question ownership. | A fresh contributor can bootstrap without inventing a cross-cutting rule. | Cairn maintainers | not-run |

## Walking skeleton / first vertical slice

The first slice is an end-to-end local commit path: a contributor starts from the repository root, mise resolves the environment, pnpm installs the workspace, a package test executes, the quality gate checks formatting/lint/dependency usage/complexity, and the commit message is validated before Git creates the commit. The contract path is the stable sequence `mise run setup` -> `mise run check` -> pre-commit `commit-msg` verification.

| Step | Boundary crossed | Test/observation | Deploy/rollback | Acceptance |
| --- | --- | --- | --- | --- |
| Bootstrap | Contributor shell to mise and pnpm workspace | `mise exec -- node --version` and frozen install output | No deployment; remove local tool cache and rerun setup if installation fails | Required tools resolve and `pnpm install --frozen-lockfile` exits 0 |
| Package test | Root recursive script to `@cairn/example` | Node test observes `identity` returning its input | No data migration; revert package files to the prior commit | `pnpm --filter @cairn/example test` exits 0 |
| Quality gate | Root scripts to Biome, Oxlint, and Knip | Formatter, recommended lint, complexity, and graph diagnostics | Revert the offending change; no auto-fix runs in the gate | `mise run check` exits 0 on clean source and non-zero on each negative fixture |
| Commit message | pre-commit `commit-msg` stage to `verify-commit` and Cocogitto | Valid and invalid message files produce distinct statuses | Re-edit the message and retry; no history rewrite is automatic | Valid Conventional Commit passes and invalid text is blocked |

## Sensors and Definition of Done

| ID | Invariant | Check or signal | When | Owner | State | Failure action |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Project tasks remain standalone executable files. | `mise tasks ls --local`, `mise tasks validate`, `mise fmt --check`, and executable mode inspection. | Every configuration change | Tooling owner | confirmed | Restore the file-task layout and executable bit; do not add `[tasks.*]` entries. |
| S2 | Workspace discovery has one authoritative package glob. | `pnpm install --frozen-lockfile` and `pnpm -r --if-present test`. | Every package change | Package owners | confirmed | Update `pnpm-workspace.yaml` and the affected lockfile together. |
| S3 | Source and config remain formatted and Biome-clean. | `pnpm run format:check` and `pnpm run lint:biome`. | Every commit | Tooling owner | confirmed | Run `mise run format` explicitly, then fix remaining diagnostics. |
| S4 | Function complexity stays at or below 20. | `pnpm run lint:oxlint` with the explicit Oxlint rule. | Every commit | Package owners | confirmed | Refactor the function or record a threshold decision before changing the rule. |
| S5 | Workspace dependency usage is declared and reachable. | `pnpm run knip` with config hints treated as errors. | Every commit | Package owners | confirmed | Add/remove the manifest entry or update a reviewed Knip configuration. |
| S6 | Commit messages follow the repository convention. | pre-commit `commit-msg` stage and `cog check`. | Every commit | Maintainers | confirmed | Amend the message; do not bypass the hook as a normal workflow. |

Definition of Done: all required records validate; `mise run setup`, `mise run check`, and `pre-commit run --all-files` pass; valid and invalid commit-message and complexity fixtures produce the expected statuses; task files retain executable mode; and every open question has an owner and next check.

## Evolution and rollback

There is no predecessor system or business data migration. Release one is the committed configuration plus the private starter package. A failed configuration change rolls back by reverting the commit, removing the local hook installation with pre-commit's normal uninstall path, and rerunning the frozen setup. A later package build or release boundary must preserve the `workspace:` contract through a compatibility checkpoint, add an ADR for versioning/bump order, and define a package-specific rollback before publishing. CI and deployment remain separate release phases.

## Open questions

| Question | Owner | Next check | State |
| --- | --- | --- | --- |
| Should Windows be a supported contributor platform? | Platform owner | Evaluate a PowerShell task pair and a cross-platform pre-commit backend before the next foundation revision. | unknown |
| What build and type-check contract should future internal packages use? | Package owners | Choose a representative package and add a bounded build/type-check probe. | unknown |
| When should Cogo monorepo bump and package release ordering begin? | Release owner | Confirm package version policy and explicit package ownership before enabling a resolver. | unknown |
| Should the complexity threshold be tightened after real package code arrives? | Tooling owner | Review Oxlint scores after the next two package increments. | inferred |
