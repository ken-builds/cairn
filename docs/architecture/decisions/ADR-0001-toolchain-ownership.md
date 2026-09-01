# ADR-0001: Use a hybrid mise and pnpm toolchain

Status: proposed
Date: 2026-09-01
Deciders: Cairn maintainers

## Context

The [monorepo Foundation Brief](../briefs/monorepo-toolchain.md) requires mise, pnpm, private workspace packages, and specialized local quality tools. The repository is greenfield, so the first choice should be reversible and should expose the dependency ownership clearly. Knip needs JavaScript tools to be visible from package manifests and scripts, while pre-commit and Cocogitto are native developer CLIs rather than npm dependencies.

## Decision

Use mise as the source of truth for Node 22, Python 3.12.14, pnpm 11.25.0, pre-commit 4.6.2, and Cocogitto 7.0.0. Use pnpm root `devDependencies` and `pnpm-lock.yaml` as the source of truth for Biome 2.5.11, Knip 6.34.0, and Oxlint 1.80.0. Declare packages only through `pnpm-workspace.yaml` with the `packages/*` glob; do not duplicate an npm/Yarn `workspaces` field in the root manifest.

## Alternatives

| Option | Why considered | Why not selected |
| --- | --- | --- |
| Hybrid mise plus pnpm | Keeps native CLIs and JavaScript dependencies in their natural managers. | Requires contributors to bootstrap two managers through one setup task. |
| All tools through mise | Appears to provide one version manifest. | Weakens pnpm/Knip visibility and introduces more backend/platform coupling. |
| All tools through npm | Appears to simplify a Node-only setup. | Does not represent pre-commit and Cocogitto's native distribution or the requested tool preference. |

## Evidence

- E1 — mise file tasks are standalone executable scripts: https://mise.jdx.dev/tasks/file-tasks.html
- E2 — pnpm workspace discovery uses `pnpm-workspace.yaml`: https://pnpm.io/workspaces
- E8 — the selected pnpm and Knip releases support the Node 22 engine range; recorded in the Foundation Brief.

## Consequences

### Benefits

- A fresh checkout has one documented `mise run setup` entry point.
- JavaScript tool binaries are declared in `package.json`, so pnpm and Knip can resolve them without hidden global state.
- Internal package discovery remains a single pnpm contract and can grow without a second manifest.

### Costs and risks

- Contributors need mise and a POSIX shell before setup.
- Node remains an LTS-major selector rather than a fully resolved `mise.lock` version.
- Moving a tool between mise and pnpm later requires updating the setup task, lockfile, and ADR.

## Confidence

High: the choice follows the supplied manager requirements and the official workspace/file-task contracts. Cross-platform support and future package build tooling remain untested assumptions.

## Revisit Trigger

Revisit when Windows support becomes a requirement, when a package needs an independent release/build toolchain, when a selected tool drops Node 22 support, or when a reproducibility incident shows that the current pins are insufficient.

## Supersedes

None - this is the initial toolchain decision.

## Superseded by

None - no later decision exists.

## Migration and rollback

The greenfield rollback is a revert of `mise.toml`, the root manifest, and the lockfile followed by a fresh `mise run setup`. A later migration can move an individual tool to another backend while preserving the root command names as a compatibility boundary.
