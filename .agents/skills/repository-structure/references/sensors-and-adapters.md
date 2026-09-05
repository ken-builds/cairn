# Structure sensors and adapters

Choose the cheapest check that observes the invariant. Keep a measured signal separate from a
semantic conclusion, and let the repository's existing tools remain authoritative for facts they
already expose.

## Sensor catalogue

| Invariant | Preferred sensor | State and failure action |
| --- | --- | --- |
| Direct growth stays reviewable | `inventory_structure.py` or a native report | Advisory signal; open a Structure Review at the configured band |
| Dependency direction remains valid | Native dependency graph, architecture test, or visibility rule | Fail the owning gate on a confirmed forbidden edge; report unknown when no graph is available |
| No dependency cycle exists | Native build/analysis check or cycle detector | Fail the structural gate and name the cycle and owner |
| Public and private paths remain intentional | Package/build/export/entrypoint check | Require a compatibility decision before a public path changes |
| Every declared boundary has an owner | `CODEOWNERS`, `OWNERS`, `MAINTAINERS`, or repository policy | Advisory until the repository declares ownership mandatory; repair the mapping |
| Boundary README paths remain valid | Markdown/link/path validator | Fail broken local references; request semantic review for changed boundary facts |
| Structure matches accepted records | Tree/Map diff in review or CI | Record drift as a superseding decision or an owned waiver |
| Historical coupling stays understood | Bounded version-control churn/co-change report | Use as evidence for review, never as an automatic move command |

## Inventory helper

The bundled `scripts/inventory_structure.py` is intentionally language-agnostic. It may measure:

- direct and recursive file counts;
- role counts for production, test, generated, vendor, documentation, tooling, and build output;
- physical text lines with binary files separated;
- relative semantic depth and child-directory fan-out;
- local README and common boundary-marker presence;
- configured include/exclude paths and threshold dispositions;
- optional `--skip-line-count` and `--no-default-excludes` modes for large or unusual trees;
  version-control metadata remains excluded in both modes.

It does not infer domain cohesion, parse imports, decide ownership, or rewrite files. Prefer
version-control tracked paths when the repository can provide them; otherwise state that the
inventory is filesystem-based. Unknown file roles remain visible in the report.

Typical read-only invocation:

```sh
python3 scripts/inventory_structure.py <repository-root> --tracked --format json
```

The command returns zero after producing a report, including when a review band is crossed. It
returns a usage/configuration error only for an invalid root or policy. A repository may wrap the
report in a CI rule after a human accepts the thresholds and repair path.

The JSON report uses a stable shape. Binary or unreadable files remain in file counts and
contribute zero to line totals.

```json
{
  "schema_version": 1,
  "root": ".",
  "filters": {
    "include": [],
    "exclude": [],
    "default_excludes": true
  },
  "thresholds": {
    "observe_direct_production_files": 8,
    "review_direct_production_files": 12,
    "compare_direct_production_files": 20
  },
  "summary": {
    "files_scanned": 0,
    "directories_scanned": 0,
    "excluded_paths": 0,
    "line_count_mode": "physical",
    "roles": {}
  },
  "directories": [
    {
      "path": "source/example",
      "depth": 2,
      "direct_files": 0,
      "direct_production_files": 0,
      "recursive_files": 0,
      "physical_lines": 0,
      "production_lines": 0,
      "child_directories": 0,
      "roles": {},
      "recursive_roles": {},
      "readme": null,
      "markers": [],
      "boundary_candidate": false,
      "disposition": "retain"
    }
  ]
}
```

The numeric values are advisory defaults. A consumer can supply a JSON policy with `thresholds`,
`exclude`, `exclude_defaults`, `role_overrides`, and `boundary_paths`; the policy format is an
adapter contract, not a new build system. Keep repository-specific path globs in the repository,
not in this skill.

## Dependency-edge adapter

When a native tool can export a graph, normalize it to this minimal input before applying boundary
rules:

```json
{
  "schema_version": 1,
  "edges": [
    {
      "source": "source/upper/file",
      "target": "source/lower/file",
      "kind": "build-or-import",
      "evidence": "native-report-or-command"
    }
  ]
}
```

Map file paths to boundary IDs before evaluating allowed edges. Keep edge extraction and policy
evaluation separate so a repository can replace its parser or build system without rewriting the
structure rules. A missing graph is `unknown`, not evidence that no forbidden edge exists.

## Ownership adapter

Discover the repository's existing ownership source in this order: explicit boundary policy,
ownership files, build/package ownership metadata, then recent review history. Preserve path
patterns and exclusions exactly; do not infer a team solely from a directory name. An ownership
gap is a review signal, while an ownership conflict on a security or release boundary is a hard
trigger.

## Public and build adapters

Identify public paths and build units from manifests, entrypoint declarations, build descriptions,
visibility settings, command registries, generated indexes, and release configuration. The adapter
reports facts and affected consumers; the Structure Review decides whether a compatibility window,
alias, redirect, or breaking decision is required.

## History adapter

Use bounded version-control queries to identify churn and co-change clusters when they can change
the candidate ranking. Record revision range, path filters, command, and limitations. A history
cluster is evidence of likely coupling, not proof of a component boundary.

## README coverage adapter

For each accepted boundary, report:

- expected local context path or `not-warranted` reason;
- whether the file exists and is readable;
- local links and referenced paths that resolve;
- the boundary facts that changed since the last review;
- owner and next semantic-review trigger.

Use `$readme-authoring` for prose and link validation when available. Keep the structure sensor
responsible for coverage and the relation to boundary IDs.

## Cadence and waivers

Run filesystem and dependency sensors locally and in the narrowest relevant CI gate. Run history
and semantic README review when a boundary changes or on the repository's chosen cadence. Every
waiver names a sensor, owner, repair path, and expiry or revisit trigger; an expired waiver returns
the signal to the review queue.
