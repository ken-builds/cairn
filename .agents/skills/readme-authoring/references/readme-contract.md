# README contract

This is the single source of truth for the README skill's audit and handoff shape.
The README itself remains ordinary Markdown; the contract keeps the writing process
traceable without adding a second repository document.

## Fact ledger

For each actionable claim, record these fields in working notes or the response:

| Field | Meaning |
| --- | --- |
| Claim | The exact statement, command, path, version, or promise planned for the README. |
| Audience job | The reader task the claim helps complete. |
| Source | Repository path, user-supplied material, or authoritative URL. |
| Freshness | Commit/version/date when the source can change. |
| State | `confirmed`, `inferred`, `unknown`, `not-run`, or `blocked`. |
| Disposition | Keep, qualify, replace, link, or omit. |
| Owner/next check | Required when the state is not `confirmed`. |

An inference may guide prose only when it is labelled or confirmed before recording.
Do not turn a missing fact into a confident command. A command that was inspected but
not executed is `not-run`, not `confirmed`.

## README spine

Use only sections that serve the selected audience and archetype. A useful default order is:

1. Identity and value — name, one-sentence purpose, audience, and a visible first result.
2. Prerequisites — supported runtime/platform, access, and required tools.
3. Installation — the shortest reproducible setup, including working directory.
4. Quick start — one copyable success path with expected result or verification.
5. Usage and configuration — common commands/API calls, options, environment variables,
   and links to deeper reference.
6. Development and tests — local setup and the repository's authoritative checks.
7. Contribution, support, security, license, and related links — include only supported
   entry points and keep policy text in its authoritative file.

The first four sections are the default reader path. A profile may merge or rename them,
but the equivalent information must remain discoverable through clear headings or links.

## Draft and record contract

The audit/preview response should state:

- target path and protected paths;
- audience, archetype, language, and success path;
- sections added, changed, retained, or omitted;
- fact-ledger exceptions and sources for dynamic claims;
- sensor command/result and optional probe state;
- exact authorization still needed, if any.

`record` is limited to the approved README path and preview. If the user requests a
different file, scope, or generated artifact, treat it as a new baseline and re-audit.

## Writing rules

- Prefer executable, copyable instructions over slogans.
- Keep one source of truth for commands, versions, policy, and API details; link rather
  than duplicate text that already lives in maintained documentation.
- Put platform-specific forks beside the command they modify.
- Use safe placeholders such as `YOUR_VALUE` only when the reader must supply a value;
  never include credentials, private URLs, or machine-specific absolute paths.
- State expected output or a verification command for the success path.
- Preserve valid anchors and canonical terminology when revising an existing README.
