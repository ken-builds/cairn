# ADR-0002: Use pre-commit as the local quality gate owner

Status: proposed
Date: 2026-09-01
Deciders: Cairn maintainers

## Context

The [monorepo Foundation Brief](../briefs/monorepo-toolchain.md) requires checks before commits and explicitly defers CI. Two installers writing the same Git hook would allow one tool to silently replace another, so hook ownership must be singular. The quality responsibilities are intentionally split: Biome for formatting and recommended lint, Oxlint for function complexity, Knip for workspace graph analysis, and Cocogitto for commit-message and history validation.

## Decision

Let pre-commit install and own both `.git/hooks/pre-commit` and `.git/hooks/commit-msg`. The `pre-commit` stage runs `mise run check` with no filename arguments; the `commit-msg` stage runs `mise run verify-commit`, which calls `cog verify --file` for the supplied message file. Keep `cog.toml` free of an installable `git_hooks.commit-msg` entry. Set Oxlint classic complexity to `max = 20` as an initial baseline and deny warnings. Do not add CI workflows or release hooks.

## Alternatives

| Option | Why considered | Why not selected |
| --- | --- | --- |
| pre-commit owns both stages | One installer, explicit stage routing, and a single aggregate check. | The hook entry depends on mise being available on PATH. |
| Cocogitto installs `commit-msg` separately | Uses Cocogitto's native hook installer. | Creates competing ownership and can overwrite the pre-commit hook file. |
| npm hook manager plus commit-message package | Keeps hook commands in the Node ecosystem. | Conflicts with the requested specialized tools and adds another lifecycle layer. |

## Evidence

- E3 — pre-commit supports local unsupported hooks and named stages: https://pre-commit.com/
- E4 — Cocogitto verifies a commit-message file with `cog verify --file`: https://docs.cocogitto.io/guide/git_hooks.html
- E7 — Oxlint complexity supports `max` and `variant`: https://oxc.rs/docs/guide/usage/linter/rules/eslint/complexity

## Consequences

### Benefits

- Every normal local commit runs the same aggregate, read-only quality gate.
- Commit-message validation and source validation cannot overwrite each other's hook files.
- The root command contracts remain usable manually without a CI-specific wrapper.

### Costs and risks

- A contributor can bypass local hooks with standard Git options, so this is not a remote enforcement boundary.
- Running Knip and the full workspace test set on every commit may become slow as the repository grows.
- The complexity threshold is a baseline and may need a measured migration when real code arrives.

## Confidence

High: stage ownership and command contracts are explicit and supported by the official tool documentation. Runtime duration and cross-platform hook behavior remain open measurements.

## Revisit Trigger

Revisit when local gate duration exceeds an agreed contributor budget, when a remote enforcement requirement appears, when hook installation conflicts with a custom `core.hooksPath`, or when complexity scores show that 20 is not a useful baseline.

## Supersedes

None - this is the initial local-gate decision.

## Superseded by

None - no later decision exists.

## Migration and rollback

Rollback removes the pre-commit installation and reverts `.pre-commit-config.yaml`, task scripts, and `cog.toml`. A future CI or release hook must call the same root `check` contract first and document how it coexists with local hook ownership.
