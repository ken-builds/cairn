# README archetype profiles

Select the narrowest profile supported by repository evidence. A repository can use a
primary profile plus a secondary one (for example, a library in a monorepo); keep the
root README's audience and success path unambiguous.

## Library

Audience: consumers and integrators. Lead with supported runtimes, installation from the
package manager, a minimal import/API example, compatibility notes, and a link to API
reference. Name the package exactly as the manifest does. Verify the import path and the
smallest callable result from examples or tests.

## CLI

Audience: operators and end users. Show installation, one safe invocation, input/output
format, `--help` or options discovery, configuration/environment variables, exit/error
behavior, and a harmless sample. Prefer commands already defined by entry points, bin
fields, Make targets, or documented examples. Do not invent flags from a framework.

## Application

Audience: people running or evaluating the application. State prerequisites, local
installation, configuration, how to start it, the URL or observable screen/result, and
the development/test path. Keep secrets and environment-specific endpoints out of the
README; point to an example configuration when one exists.

## Service

Audience: developers and operators. Include local dependencies, configuration and secret
boundaries, health/readiness or first request, logs/observability entry points, test and
container/deploy commands that are actually present, and a safe shutdown/cleanup note.
Avoid promising production topology or SLOs unless an authoritative source states them.

## Template

Audience: people generating a new project. Explain prerequisites, generation command,
input variables, produced layout, the first command in the generated project, and how to
update the template. Keep template markers in examples only when they are intentional and
not unresolved placeholders in reader-facing prose.

## Monorepo

Audience: repository users plus package owners. Explain workspace/package discovery,
root-level install/bootstrap, how to run or test one package, how to run the aggregate
checks, and where package-specific READMEs live. Use a table or short map only when it
reduces navigation cost. Do not duplicate every package README at the root.

## Ambiguous or mixed repositories

When evidence supports multiple profiles, choose the path that matches the requested
reader job and say which secondary paths are intentionally linked or deferred. If the
choice would change installation commands or public promises, mark it `unknown` and ask
before recording.
