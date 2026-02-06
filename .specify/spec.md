# Specification: Domain Model Refactoring

**Feature ID:** CORE-004  
**Issue:** [#4 - Domain Model Refactoring](https://github.com/vindicta-platform/Vindicta-Core/issues/4)  
**Milestone:** v0.2.0 Refactor  
**Priority:** P1  
**Status:** Draft  

---

## 1. Problem Statement

The current `vindicta_core` package has a **monolithic structure** where all domain models reside in a single `models.py` file (145 lines) and all interface contracts in a single `interfaces.py` file (113 lines). As the platform grows, this structure will:

- Create **coupling** between unrelated domain concepts
- Increase **circular import risk** between modules
- Make **navigation and maintenance** increasingly difficult
- Violate **separation of concerns** for downstream consumers (API, AI engines, notation tools)

---

## 2. Vision

Decompose the monolithic model file into **domain-organized subpackages** that:
- Group related models by business domain
- Establish clear dependency direction (no circular imports)
- Enable selective imports for downstream consumers
- Maintain backward compatibility for existing integrations

---

## 3. User Stories

### US-01: Platform Developer
> As a **platform developer** working on Vindicta-API,  
> I want to **import only the Gas Tank models** I need,  
> So that **my import statements are clean and my module dependencies are explicit**.

**Acceptance Criteria:**
- [ ] `from vindicta_core.gas_tank import GasTankState, CostEstimate` works
- [ ] Importing gas tank models does NOT import dice/entropy models

### US-02: AI Engine Developer
> As an **AI engine developer** working on Primordia-AI,  
> I want to **import evaluation interfaces without pulling in unrelated protocols**,  
> So that **my dependency graph remains minimal and testable**.

**Acceptance Criteria:**
- [ ] Interfaces can be imported from domain-specific modules
- [ ] No unnecessary transitive dependencies

### US-03: Maintainer
> As a **codebase maintainer**,  
> I want **models organized by domain (dice, gas_tank, base)**,  
> So that **I can navigate and modify related code without touching unrelated domains**.

**Acceptance Criteria:**
- [ ] Models organized into subpackages by domain
- [ ] Each subpackage has its own `__init__.py` with clear exports
- [ ] File structure matches logical domain boundaries

### US-04: Backward Compatibility
> As an **existing consumer** of `vindicta_core`,  
> I want **current import paths to continue working**,  
> So that **I don't have to update all my existing code immediately**.

**Acceptance Criteria:**
- [ ] `from vindicta_core.models import GasTankState` still works
- [ ] `from vindicta_core.interfaces import DiceEngineProtocol` still works
- [ ] Deprecation warnings (optional) guide users to new paths

---

## 4. Proposed Domain Decomposition

| Domain | Models | Interfaces |
|--------|--------|------------|
| `base` | `VindictaModel`, `TimestampedModel`, `IdentifiableModel` | — |
| `dice` | `EntropyProof`, `DiceResult` | `DiceEngineProtocol`, `BaseDiceEngine` |
| `gas_tank` | `GasTankState`, `CostEstimate` | `GasTankProtocol`, `BaseGasTank` |
| `oracle` | — | `OracleProtocol` |

---

## 5. Non-Goals

- **No behavioral changes**: All models/interfaces keep identical logic
- **No new features**: This is purely structural refactoring
- **No breaking changes**: All current imports must continue to work

---

## 6. Constraints

- **Constitution Compliance**: Maintain alignment with Constitution VII (Mechanical Fidelity) and XVI (Async-First)
- **Test Preservation**: All 29 existing tests must pass unchanged
- **No New Dependencies**: Zero new external packages

---

## 7. Open Questions

1. Should deprecated import paths emit `DeprecationWarning` or remain silent?
2. Should domain subpackages also include `py.typed` marker for type-checking?
3. What is the timeline for eventually removing backward-compat shims?

---

## 8. Clarification Cycle 1: Ambiguity Search

### Identified Ambiguities

| Term | Ambiguity | Resolution |
|------|-----------|------------|
| "Domain-organized subpackages" | Unclear if these are nested directories or flat modules | **Resolution**: Nested directory structure (e.g., `vindicta_core/dice/`) with `__init__.py` for each |
| "Backward compatibility" | Unclear scope - all public symbols or just documented API? | **Resolution**: All currently exported symbols in `__init__.py` must remain accessible |
| "Clear dependency direction" | No explicit rule stated | **Resolution**: Base → Domain-specific (one-way). Domain modules may import from `base`, never reverse |
| "Selective imports" | Unclear if lazy loading is required | **Resolution**: Eager loading acceptable; goal is to avoid importing *unrelated* domains |

### Decisions Made

1. **Package Structure**: Use proper Python subpackages (directories with `__init__.py`), not namespace packages
2. **Re-exports**: Root `models.py` and `interfaces.py` will re-export all symbols for backward compatibility
3. **Dependency Rule**: `base` has zero internal imports. All other domains may only import from `base`

---

## 9. Clarification Cycle 2: Component Impact

### Files Requiring Modification

| File | Change Type | Impact |
|------|-------------|--------|
| `src/vindicta_core/models.py` | **REFACTOR** | Split into domain submodules, retain as re-export shim |
| `src/vindicta_core/interfaces.py` | **REFACTOR** | Split into domain submodules, retain as re-export shim |
| `src/vindicta_core/__init__.py` | **MODIFY** | Update exports to include new subpackages |
| `src/vindicta_core/base/__init__.py` | **NEW** | Base models (VindictaModel, TimestampedModel, IdentifiableModel) |
| `src/vindicta_core/dice/__init__.py` | **NEW** | EntropyProof, DiceResult, DiceEngineProtocol, BaseDiceEngine |
| `src/vindicta_core/gas_tank/__init__.py` | **NEW** | GasTankState, CostEstimate, GasTankProtocol, BaseGasTank |
| `src/vindicta_core/oracle/__init__.py` | **NEW** | OracleProtocol |
| `tests/test_models.py` | **VERIFY** | Must pass unchanged (import compatibility) |

### Downstream Consumer Impact

| Consumer | Integration Point | Required Action |
|----------|-------------------|-----------------|
| Vindicta-API | `from vindicta_core.models import *` | None (backward compat) |
| WARScribe-Core | `from vindicta_core.models import VindictaModel` | None (backward compat) |
| Primordia-AI | `from vindicta_core.interfaces import *` | None (backward compat) |

---

## 10. Clarification Cycle 3: Edge Case / Failure Analysis

### Potential Failure Modes

| Scenario | Risk | Mitigation |
|----------|------|------------|
| Circular import between domains | **HIGH** | Strict rule: domains import only from `base`, never from each other |
| Test imports break | **MEDIUM** | Backward-compat shim ensures all current imports work |
| Type checker cannot resolve new paths | **LOW** | Add `py.typed` marker to each subpackage |
| IDE autocomplete breaks | **LOW** | Proper `__all__` exports in each `__init__.py` |
| Installation from GitHub breaks | **LOW** | Verify `uv pip install git+...` after refactor |

### Edge Cases

1. **Dynamic imports**: If any consumer uses `importlib.import_module('vindicta_core.models')`, it will still work
2. **Star imports**: `from vindicta_core.models import *` must expose same symbols as before
3. **Type annotations**: Forward references like `'DiceResult'` must resolve correctly
4. **Pickle compatibility**: Serialized objects with old class paths may fail to deserialize (acceptable risk)

### Mitigations Implemented

- [ ] Root `models.py` re-exports all symbols with `__all__` list
- [ ] Root `interfaces.py` re-exports all symbols with `__all__` list  
- [ ] Each domain `__init__.py` has explicit `__all__` exports
- [ ] All 29 existing tests pass without modification
