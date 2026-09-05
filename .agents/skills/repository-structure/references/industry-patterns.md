# Industry patterns for repository structure

These sources are evidence for mechanisms, not templates to copy. The skill remains language- and
build-system-agnostic. External claims were checked on 2026-09-04; re-check dynamic details before
using them for a current repository decision.

## Linux kernel

- The source tree groups major areas by subsystem, architecture, and repository role rather than
  by numbered dependency levels: [Linux source tree](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/).
- Kbuild describes Makefiles in every subdirectory and recursive descent controlled by the build
  configuration, making a subdirectory a possible build boundary: [Linux Kernel Makefiles](https://docs.kernel.org/kbuild/makefiles.html).
- `MAINTAINERS` maps path patterns, exclusions, status, lists, and maintainer trees; the path is a
  routing and ownership index, not merely a visual grouping: [MAINTAINERS](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/MAINTAINERS).
- Subsystem-specific profiles add local process, testing, and review expectations: [Maintainer
  Entry Profile](https://docs.kernel.org/maintainer/maintainer-entry-profile.html).

The transferable lesson is to align the tree with subsystem ownership and build/review boundaries,
then use explicit metadata and checks for the rules. Linux's exact names and depth are not a
portable project template.

## Gradual package boundaries

The official Go layout guide starts with a simple package in one directory, then introduces
supporting internal packages and separate subpackages as size and reuse grow: [Organizing a Go
module](https://go.dev/doc/modules/layout). The useful principle is evolutionary pressure, not a
specific language convention: begin with the smallest coherent boundary and split when a new
boundary protects consumers or reduces local coupling.

## Machine-enforced directory boundaries

Bazel defines a package as a directory containing a build description and uses visibility to limit
which packages can depend on targets: [Repositories, workspaces, packages, and targets](https://bazel.build/concepts/build-ref#packages), [Visibility](https://bazel.build/concepts/visibility).
This illustrates how a physical directory can become a machine-enforced boundary when the build
system gives it that meaning.

## Path ownership and local documentation

GitHub documents path-pattern ownership and required code-owner review through `CODEOWNERS`:
[About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
GitHub's README guidance also supports concise getting-started context and relative links between
repository documents: [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

## Coding-agent context

An engineering report on long-running coding agents describes fresh sessions starting without the
previous context and uses durable, clear artifacts plus incremental progress to reduce repeated
reconstruction: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
This supports co-located boundary context as a useful mechanism, while leaving the exact filename
and loading policy to the host repository.

## Synthesis

Across these examples, the durable pattern is:

1. organize by capability, subsystem, ownership, or build unit;
2. keep the hierarchy shallow enough for navigation;
3. express dependency and visibility rules in machine-readable checks;
4. keep local context beside the boundary and global rationale in global records;
5. evolve through small, reversible changes with an explicit transition state.
