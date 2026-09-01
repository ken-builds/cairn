# Foundation Brief: document-collaboration

Status: draft
Date: 2026-08-30
Owner: Platform team

## Objective
Design a foundation for a document-collaboration product that lets a small team create,
share, and review documents with an observable first release boundary.

## Non-goals
Real-time cursors, offline editing, billing, and production implementation are deferred.

## Mandate and baseline
The sponsor needs a web-accessible service for internal teams. The supplied product brief and
privacy requirements are the baseline. The target is a new repository with one platform team;
design authorization is active and no protected code changes exist.

## Constraints and assumptions
| ID | Constraint or assumption | Impact if false | Validation/owner | State |
| --- | --- | --- | --- | --- |
| A1 | The first release serves one regional tenant group. | Data placement and topology may change. | Product owner validates regional scope. | inferred |
| A2 | Review actions need transactional consistency. | The storage candidate may change. | Domain owner confirms review invariants. | unknown |

## Context Map
Authors and reviewers use the product through a browser. An identity provider supplies user
identity. The collaboration system owns documents and review decisions; the identity provider
owns accounts. The initial deployment is one application boundary with a separate database
boundary and an explicit audit boundary.

## Glossary
| Term | Scope | Canonical meaning | Source | Aliases/relations |
| --- | --- | --- | --- | --- |
| Document | collaboration domain | Versioned content owned by a workspace. | product brief | file, draft |
| Review decision | collaboration domain | An accepted or rejected review outcome attached to a document version. | domain workshop | approval |

## Drivers and scenarios
| ID | Stimulus | Context | Response | Metric | Threshold | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Reviewer submits a decision. | Valid authenticated workspace member. | Decision is stored once and visible on reload. | p95 write-to-read latency | under 500 ms at 20 requests per second | P0 |
| D2 | A deployment introduces a contract error. | First release rollback is requested. | Previous release remains usable without data corruption. | rollback recovery time | under 10 minutes in rehearsal | P1 |

## Candidates
| ID | Option | Fit | Trade-offs | Reversibility | State |
| --- | --- | --- | --- | --- | --- |
| C0 | Modular monolith with one authoritative relational store. | Fast first slice and clear domain modules. | Shared process and coordinated release. | Modules and contracts can be split later. | inferred |
| C1 | Multiple independently deployed services from the first release. | Strong isolation if teams or scale differ. | Higher operational and contract overhead. | Service boundaries are costly to reunify. | inferred |

## Foundation Blueprint
| Concern | Target shape | Owner | Evidence/state |
| --- | --- | --- | --- |
| Boundaries | Workspace, document, and review modules in one deployable. | Architecture owner | inferred |
| Dependency direction | UI and adapters depend on application policies; domain does not import infrastructure. | Architecture owner | confirmed |
| Interfaces/contracts | Versioned HTTP API with explicit error and authorization semantics. | API owner | inferred |
| Data ownership | Review module owns decisions; one relational source of truth per workspace. | Data owner | inferred |
| Runtime/deployment | Reproducible dev, test, and production environments with one release unit. | Platform owner | inferred |
| Security/trust | Identity provider authenticates; application authorizes workspace actions; audit boundary records decisions. | Security owner | unknown |
| Observability | Structured request/audit logs, latency and error metrics, health check, and alert owner. | Operations owner | inferred |
| Delivery/release | CI runs contract and integration checks; deployment has health gate and rollback command. | Platform owner | inferred |
| Cost/capacity | Start within the team cloud budget and measure database saturation before scaling out. | Platform owner | unknown |

## Evidence
| ID | Claim | Source | Version/commit | Accessed/measured | State | Applicability |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | The product brief requires transactional review decisions. | supplied product brief | not stated | 2026-08-30 | confirmed | review module |

## Probes
| ID | Question | Hypothesis | Workload/input | Environment | Baseline | Method/budget | Threshold | Result | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Can the selected store meet the write/read threshold? | C0 stays below the p95 target at the first-release load. | 20 review writes/second with reads | scratch runtime | no measurement | 5 minute run, 1 warm-up, 3 repetitions | p95 under 500 ms | not run yet | not-run |

## Decision
Selected candidate: C0

Rationale: C0 satisfies the P0 consistency and delivery drivers with the smallest reversible
operational surface.

Sensitivity points: Independent scaling, fault isolation, or team ownership may justify C1.

ADR links: None — not applicable until the sponsor accepts the durable boundary decision.

Deferred/rejected: Real-time collaboration and multi-region deployment are deferred.

## Bootstrap plan and gates
| Gate | Entry | Deliverables | Exit criterion | Owner | State |
| --- | --- | --- | --- | --- | --- |
| G0 Mandate | Product brief exists. | Objective, users, constraints, assumptions. | Success boundary and material constraints are named. | Product owner | confirmed |
| G1 Context and boundaries | G0 complete. | Map, Glossary, journeys, trust and data ownership. | Every important concept has an owner and direction. | Domain owner | confirmed |
| G2 Blueprint and decisions | G1 complete. | Candidate matrix, blueprint, decision rationale. | Hard drivers have thresholds and C0 is selected. | Architecture owner | inferred |
| G3 Walking skeleton | G2 complete. | First slice, contracts, test/deploy/observe/rollback path. | One end-to-end review outcome is observable. | Delivery owner | not-run |
| G4 Handoff | G3 complete or probe status recorded. | Brief, ADRs, increments, sensors, open questions. | Implementer can start without inventing a cross-cutting rule. | Platform team | not-run |

## Walking skeleton / first vertical slice
The first slice is an end-to-end reviewer decision path from browser request through authorization,
review policy, contract validation, data persistence, audit, and response. The test runs through
the deploy health gate, observes the audit signal, and exercises rollback.

| Step | Boundary crossed | Test/observation | Deploy/rollback | Acceptance |
| --- | --- | --- | --- | --- |
| Submit review decision | API contract to review module, data store, and audit boundary | Contract and integration test; observe the audit event | Deploy through a health gate and exercise previous-version rollback | Decision is visible once after reload within the D1 threshold |

## Sensors and Definition of Done
| ID | Invariant | Check or signal | When | Owner | State | Failure action |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | Domain modules do not import infrastructure directly. | Dependency-direction rule in CI. | every change | Architecture owner | confirmed | Move the dependency behind an adapter and update the ADR if boundary changes. |
| S2 | A review decision is recorded exactly once. | Contract/integration test plus duplicate metric. | CI and runtime | Data owner | inferred | Inspect idempotency key handling and reconcile affected records. |

Definition of Done: Required sections validate, G0 through G4 have owners, the first slice has an
acceptance path, and every unknown has an owner or a probe.

## Evolution and rollback
Release one uses one deployable and one authoritative store. A health-gated deployment can
return to the previous release; schema changes remain backward compatible through the first
checkpoint. A later module split requires a new ADR and a rebuild/reconciliation path.

## Open questions
- Confirm regional data placement — owner: Product owner; next check: privacy review on 2026-09-05; state: unknown
