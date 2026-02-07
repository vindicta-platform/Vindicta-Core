# Feature Specification: Event Sourcing Primitives

**Feature Branch**: `040-event-sourcing`
**Created**: 2026-02-06
**Status**: Draft
**Target**: Week 4 | **Repository**: Vindicta-Core

## User Scenarios & Testing

### User Story 1 - Append Events (Priority: P1)

System stores domain events immutably.

**Acceptance Scenarios**:
1. **Given** domain event, **When** appended, **Then** stored in log
2. **Given** event log, **When** replayed, **Then** state reconstructed

---

## Requirements

### Functional Requirements
- **FR-001**: Store MUST append events immutably
- **FR-002**: Store MUST support replay from any point
- **FR-003**: Store MUST track event ordering

### Key Entities
- **DomainEvent**: type, payload, timestamp, aggregateId
- **EventStore**: append(), replay(), getStream()

## Success Criteria
- **SC-001**: Append in <10ms
- **SC-002**: Replay 1000 events in <500ms
