# Tasks: Event Sourcing Primitives

**Input**: specs/040-event-sourcing/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/events/` directory
- [ ] T002 [P] Create SQLite schema

---

## Phase 2: Foundational

- [ ] T003 Define DomainEvent model
- [ ] T004 [P] Initialize EventStore class

---

## Phase 3: User Story 1 - Append Events (P1) 🎯 MVP

- [ ] T005 [US1] Implement `append()` method
- [ ] T006 [US1] Implement `getStream()` method
- [ ] T007 [US1] Implement `replay()` method
- [ ] T008 [US1] Track event ordering

---

## Phase 4: Polish

- [ ] T009 [P] Optimize replay for <500ms
- [ ] T010 [P] Write event sourcing tests
