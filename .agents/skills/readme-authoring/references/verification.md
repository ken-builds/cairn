# README verification

Verification has two layers. The sensor is deterministic and repository-local; the
probe is optional, authorized execution in a disposable boundary.

## Sensor

Run:

```text
python scripts/validate_readme.py README.md --profile auto
```

The sensor checks Markdown structure and repository consistency without network access:

- exactly one ATX H1 and a non-empty opening description;
- required installation and success-path information;
- balanced fenced code blocks;
- valid external URL syntax and existing relative link targets;
- referenced repository paths, scripts, and manifest names when they are explicit;
- unresolved TODO/template markers, accidental credentials, and machine-specific paths;
- the minimum profile-specific sections when a profile is explicit or confidently detected;
  conditional configuration, support, and policy sections are reviewed from repository facts.

`--strict` adds repository path and install-package consistency checks. A clean sensor
result does not prove that commands succeed; report that distinction.

## Probe

Request explicit `probe` authorization before installing dependencies, accessing the
network, starting containers, or running commands with side effects. Use a disposable
temporary directory or isolated environment, copy only the minimum inputs, pin or record
runtime versions, set a timeout, and define cleanup before starting. Use fake/local
credentials and local fixtures. Do not use production endpoints or write to the real
worktree.

Record the exact command, environment, exit status, observable result, duration/timeout,
network or dependency assumptions, and cleanup result. A successful setup with an
unverified first result is not a confirmed success path. Classify unavailable execution
as `not-run`; classify a missing permission, dependency, or safe boundary as `blocked`.

## External facts

Only research dynamic facts that can change a reader's action, such as supported runtime
versions, package installation syntax, hosted service URLs, or current badges. Prefer
official documentation and release notes. Record URL, version/commit, access date, and
the exact claim. A network check is evidence for that access, not a permanent guarantee.
