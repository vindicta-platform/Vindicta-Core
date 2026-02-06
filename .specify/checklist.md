# Verification Checklist: Domain Model Refactoring

**Spec Reference:** [spec.md](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/.specify/spec.md)
**Issue:** [#4](https://github.com/vindicta-platform/Vindicta-Core/issues/4)

---

## Acceptance Criteria (from Issue #4)

- [ ] ✅ Models organized by domain
- [ ] ✅ Clear dependency direction
- [ ] ✅ No circular imports

---

## User Story Verification

### US-01: Platform Developer - Selective Imports
- [ ] `from vindicta_core.gas_tank import GasTankState, CostEstimate` works
- [ ] Importing gas tank models does NOT import dice/entropy models

### US-02: AI Engine Developer - Minimal Dependencies
- [ ] `from vindicta_core.dice import DiceEngineProtocol` works
- [ ] OracleProtocol can be imported independently

### US-03: Maintainer - Domain Organization
- [ ] `src/vindicta_core/base/` directory exists with `__init__.py`
- [ ] `src/vindicta_core/dice/` directory exists with `__init__.py`
- [ ] `src/vindicta_core/gas_tank/` directory exists with `__init__.py`
- [ ] `src/vindicta_core/oracle/` directory exists with `__init__.py`

### US-04: Backward Compatibility
- [ ] `from vindicta_core.models import GasTankState` works
- [ ] `from vindicta_core.models import DiceResult` works
- [ ] `from vindicta_core.interfaces import DiceEngineProtocol` works

---

## Technical Verification

### Test Suite
- [ ] All 29 existing tests pass: `uv run pytest tests/ -v`
- [ ] No test file modifications required

### Import Checks
- [ ] Backward-compat models import:
  ```
  python -c "from vindicta_core.models import *; print('OK')"
  ```
- [ ] Backward-compat interfaces import:
  ```
  python -c "from vindicta_core.interfaces import *; print('OK')"
  ```
- [ ] New domain imports:
  ```
  python -c "from vindicta_core.base import VindictaModel; from vindicta_core.dice import DiceResult; from vindicta_core.gas_tank import GasTankState; from vindicta_core.oracle import OracleProtocol; print('OK')"
  ```

### Package Integrity
- [ ] No circular imports: `python -c "import vindicta_core"`
- [ ] Package installs: `uv pip install .`
- [ ] Package version unchanged in `__init__.py`

---

## Edge Case Checks

- [ ] Dynamic import works: `importlib.import_module('vindicta_core.models')`
- [ ] Star import exposes same symbols as before
- [ ] Type annotations resolve correctly

---

## Sign-off

| Criterion | Status | Verified By |
|-----------|--------|-------------|
| Models organized by domain | ⬜ | — |
| Clear dependency direction | ⬜ | — |
| No circular imports | ⬜ | — |
| All tests pass | ⬜ | — |
| Backward compatibility | ⬜ | — |
