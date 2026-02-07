# Tasks: Domain Model Refactoring

**Plan Reference:** [plan.md](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/.specify/plan.md)
**Issue:** [#4](https://github.com/vindicta-platform/Vindicta-Core/issues/4)

---

## Task Breakdown

### T-001: Create `base/` Subpackage
**Priority:** P0 (Foundation - must be first)
**Estimate:** 15 min

- [ ] Create `src/vindicta_core/base/__init__.py`
- [ ] Move `VindictaModel`, `TimestampedModel`, `IdentifiableModel` from `models.py`
- [ ] Add `__all__` export list
- [ ] Verify no internal imports (leaf module)

---

### T-002: Create `dice/` Subpackage
**Priority:** P1
**Estimate:** 20 min
**Depends on:** T-001

- [ ] Create `src/vindicta_core/dice/__init__.py`
- [ ] Move `EntropyProof`, `DiceResult` from `models.py`
- [ ] Move `DiceEngineProtocol`, `BaseDiceEngine` from `interfaces.py`
- [ ] Import `VindictaModel` from `base`
- [ ] Add `__all__` export list

---

### T-003: Create `gas_tank/` Subpackage
**Priority:** P1
**Estimate:** 20 min
**Depends on:** T-001

- [ ] Create `src/vindicta_core/gas_tank/__init__.py`
- [ ] Move `GasTankState`, `CostEstimate` from `models.py`
- [ ] Move `GasTankProtocol`, `BaseGasTank` from `interfaces.py`
- [ ] Import `VindictaModel` from `base`
- [ ] Add `__all__` export list

---

### T-004: Create `oracle/` Subpackage
**Priority:** P1
**Estimate:** 10 min
**Depends on:** None

- [ ] Create `src/vindicta_core/oracle/__init__.py`
- [ ] Move `OracleProtocol` from `interfaces.py`
- [ ] Add `__all__` export list

---

### T-005: Refactor `models.py` to Re-export Shim
**Priority:** P2
**Estimate:** 10 min
**Depends on:** T-001, T-002, T-003

- [ ] Replace model definitions with imports from new subpackages
- [ ] Define `__all__` with all original exports
- [ ] Add deprecation docstring (optional)

---

### T-006: Refactor `interfaces.py` to Re-export Shim
**Priority:** P2
**Estimate:** 10 min
**Depends on:** T-002, T-003, T-004

- [ ] Replace interface definitions with imports from new subpackages
- [ ] Define `__all__` with all original exports
- [ ] Remove unused imports (`ABC`, `Protocol`, etc.)

---

### T-007: Update Package `__init__.py`
**Priority:** P2
**Estimate:** 5 min
**Depends on:** T-001, T-002, T-003, T-004

- [ ] Add new subpackages to exports (optional)
- [ ] Verify version string unchanged

---

### T-008: Verification Suite
**Priority:** P0 (Gate for merge)
**Estimate:** 15 min
**Depends on:** T-005, T-006

- [ ] Run existing pytest suite: `uv run pytest tests/ -v`
- [ ] Run backward-compat import check
- [ ] Run new domain import check
- [ ] Run circular import check
- [ ] Verify `uv pip install .` works

---

## Summary

| Task | Title | Priority | Depends On | GitHub Issue |
|------|-------|----------|------------|--------------|
| T-001 | Create `base/` subpackage | P0 | — | [#7](https://github.com/vindicta-platform/Vindicta-Core/issues/7) |
| T-002 | Create `dice/` subpackage | P1 | T-001 | [#8](https://github.com/vindicta-platform/Vindicta-Core/issues/8) |
| T-003 | Create `gas_tank/` subpackage | P1 | T-001 | [#9](https://github.com/vindicta-platform/Vindicta-Core/issues/9) |
| T-004 | Create `oracle/` subpackage | P1 | — | [#10](https://github.com/vindicta-platform/Vindicta-Core/issues/10) |
| T-005 | Refactor `models.py` shim | P2 | T-001, T-002, T-003 | [#11](https://github.com/vindicta-platform/Vindicta-Core/issues/11) |
| T-006 | Refactor `interfaces.py` shim | P2 | T-002, T-003, T-004 | [#12](https://github.com/vindicta-platform/Vindicta-Core/issues/12) |
| T-007 | Update package `__init__.py` | P2 | T-001..T-004 | [#13](https://github.com/vindicta-platform/Vindicta-Core/issues/13) |
| T-008 | Verification suite | P0 | T-005, T-006 | [#14](https://github.com/vindicta-platform/Vindicta-Core/issues/14) |
