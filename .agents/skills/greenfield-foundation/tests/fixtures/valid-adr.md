# ADR-0001: Start with a modular monolith

Status: proposed
Date: 2026-08-30
Deciders: Platform team

## Context
The Foundation Brief needs a fast, reversible first release for a small team. The P0 drivers
favor transactional review decisions and a short delivery path. The Brief records C0 and the
remaining scaling assumptions.

## Decision
Start with a modular monolith whose domain modules own their policies and a single authoritative
relational store owns transactional review data. Preserve one-way dependencies so a later split
does not require changing domain contracts.

## Alternatives
| Option | Why considered | Why not selected |
| --- | --- | --- |
| Modular monolith | Meets first-release consistency and delivery drivers. | Requires a coordinated deploy. |
| Independent services | Offers separate scaling and fault boundaries. | No current driver offsets its operational and contract overhead. |

## Evidence
- E1 — The supplied product brief requires transactional review decisions; recorded in the Foundation Brief.

## Consequences
### Benefits
- The first slice has one deployable and a clear consistency owner.
- Module contracts and dependency rules preserve a later extraction path.
### Costs and risks
- A process failure can affect multiple modules until a separate boundary is justified.
- The storage and capacity assumptions still need probe P1.

## Confidence
Medium: the P0 requirements and team shape support the choice, but capacity and regional
placement remain untested assumptions.

## Revisit Trigger
Revisit when sustained p95 exceeds the D1 threshold, an independent release or security boundary
is required, or the team adds an owner for a separately operated service.

## Supersedes
None — this is the initial decision.

## Superseded by
None — no later decision exists.

## Migration and rollback
Keep the first schema backward compatible through the first release checkpoint. A failed deploy
rolls back to the previous application version; a later module extraction requires a new ADR,
dual-read/write or rebuild plan, and a rehearsed rollback.
