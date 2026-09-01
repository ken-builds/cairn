# Cairn

Cairn is a pnpm workspace for private packages with a reproducible mise-managed development environment and local quality gates.

## Prerequisites

Install [mise](https://mise.jdx.dev/) and use a POSIX shell on macOS or Linux. Node.js, pnpm, Python, pre-commit, and Cocogitto are installed from the project configuration; do not rely on Corepack or globally installed Node tools.

## Installation

From the repository root, bootstrap the pinned environment, workspace dependencies, and Git hooks:

```sh
mise run setup
```

The setup task installs both the `pre-commit` and `commit-msg` hook types. With the committed `pnpm-lock.yaml` it uses a frozen install; a brand-new checkout without a lockfile generates one on the first run.

## Quick start

Run the complete local gate:

```sh
mise run check
```

The command must exit with status 0. It validates task scripts and configuration, runs the package tests, checks formatting and lint rules, checks the workspace dependency graph, and verifies the existing Conventional Commit history.

## Workspace layout

| Path | Purpose |
| --- | --- |
| `packages/*` | Private internal workspace packages discovered by pnpm |
| `.mise/tasks` | Executable mise file tasks |
| `docs/architecture` | Foundation Brief and Architecture Decision Records |

The starter package is `@cairn/example`. It is a toolchain fixture, not a product API. Package-to-package dependencies should use pnpm's `workspace:` protocol.

## Usage

Run one package's tests with:

```sh
pnpm --filter @cairn/example test
```

Useful root commands are:

```sh
pnpm run format       # write Biome formatting changes
pnpm run format:check # check formatting without writing
pnpm run lint         # Biome lint plus Oxlint complexity
pnpm run knip         # inspect package and dependency usage
pnpm run test         # run tests in every package that defines one
```

Oxlint enforces classic cyclomatic complexity at a maximum of 20. Biome owns formatting and recommended lint rules; Knip owns workspace dependency and export analysis.

## Development

The aggregate `mise run check` task is the required local quality gate. `mise run format` is the explicit write path; the check and hook paths are read-only. Run `mise fmt --check` and `mise tasks validate` when changing `mise.toml` or a file task.

## Commit conventions

Commits follow the Conventional Commits format, for example:

```text
feat: add a package
fix(example): correct the identity fixture
```

The pre-commit framework owns both local hook files. The `commit-msg` stage delegates message validation to Cocogitto. There is intentionally no CI configuration yet.

## Architecture records

The current foundation and its durable choices are recorded in [`docs/architecture/briefs/monorepo-toolchain.md`](docs/architecture/briefs/monorepo-toolchain.md), [`ADR-0001`](docs/architecture/decisions/ADR-0001-toolchain-ownership.md), and [`ADR-0002`](docs/architecture/decisions/ADR-0002-local-quality-gates.md).
