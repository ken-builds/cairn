# Implementation Record: example-boundary

Date: 2026-09-04
Owner: Example team
Status: complete
Baseline: `main@0123456789abcdef`
Authorization: implementation and documentation

## Purpose

Preserve the non-obvious validation and commit-order rationale for the example increment.

## Scope

The increment validates input before publishing committed state. The record summarizes public API
coverage without duplicating the source documentation; deployment configuration remains outside.

## Inputs

The implementation follows the [example decision](./decision.md) and the checked-in tests.

## Public API coverage

| Surface | Kind | Scope | Documentation | Coverage check | State |
| --- | --- | --- | --- | --- | --- |
| `ExampleApi` | exported type | one public result member | source declaration | `python3 -m unittest` | confirmed |

## Implementation sequence

Validation was completed before the commit path because failed input must leave no published
state.

## Rationale ledger

| ID | Finding/observation | Evidence | Impact if changed | Placement | State |
| --- | --- | --- | --- | --- | --- |
| R1 | The adapter accepts a wider input shape than the public boundary. | focused negative test | Invalid data could reach storage. | source comment and negative test | confirmed |
| R2 | State is published only after the commit succeeds. | injected commit failure | Callers could observe uncommitted state. | decision link and fault test | inferred |

## Comment and sensor map

| ID | Source location | Role | Link or check | State |
| --- | --- | --- | --- | --- |
| R1 | `./sample.py:1` | source rationale | `python3 -m unittest` | confirmed |
| R2 | [example decision](./decision.md) | decision and sensor | injected commit failure | inferred |

## Verification

| Check | Command | Environment | Result | State |
| --- | --- | --- | --- | --- |
| validator tests | `python3 -m unittest` | Python 3 standard library | all focused checks passed | confirmed |

## Drift and decisions

None - the implementation follows the accepted example decision.

## Remaining boundaries

None - the example fixture has no production boundary.
