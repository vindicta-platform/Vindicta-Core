# Implementation Plan: Domain Model Refactoring

**Spec Reference:** [spec.md](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/.specify/spec.md)  
**Issue:** [#4 - Domain Model Refactoring](https://github.com/vindicta-platform/Vindicta-Core/issues/4)  
**Milestone:** v0.2.0 Refactor  

---

## Goal

Decompose the monolithic `models.py` and `interfaces.py` into domain-organized subpackages while maintaining full backward compatibility with existing imports.

---

## Proposed Changes

### Base Domain (`base/`)

#### [NEW] [__init__.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/base/__init__.py)

Extract foundational models:
- `VindictaModel` - Base Pydantic model with JSON encoders
- `TimestampedModel` - Adds `created_at`/`updated_at` fields
- `IdentifiableModel` - Adds UUID `id` field

**Dependencies:** None (leaf module)

---

### Dice Domain (`dice/`)

#### [NEW] [__init__.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/dice/__init__.py)

Extract entropy and dice models/interfaces:
- `EntropyProof` - Cryptographic proof for randomness (Constitution VI)
- `DiceResult` - Roll result with embedded proof
- `DiceEngineProtocol` - Protocol for dice services
- `BaseDiceEngine` - Abstract base with `roll_d6`/`roll_d3` implementations

**Dependencies:** `base.VindictaModel`

---

### Gas Tank Domain (`gas_tank/`)

#### [NEW] [__init__.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/gas_tank/__init__.py)

Extract cost control models/interfaces:
- `GasTankState` - Current balance and limits (Constitution II)
- `CostEstimate` - Pre-execution cost evaluation
- `GasTankProtocol` - Protocol for tank services
- `BaseGasTank` - Abstract base for implementations

**Dependencies:** `base.VindictaModel`

---

### Oracle Domain (`oracle/`)

#### [NEW] [__init__.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/oracle/__init__.py)

Extract AI oracle interface:
- `OracleProtocol` - Protocol for Gemini-powered AI services

**Dependencies:** None (standalone protocol)

---

### Backward Compatibility Shims

#### [MODIFY] [models.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/models.py)

Refactor to re-export all symbols from new locations:

```python
"""Backward-compatible re-exports for vindicta_core.models."""

from vindicta_core.base import VindictaModel, TimestampedModel, IdentifiableModel
from vindicta_core.dice import EntropyProof, DiceResult
from vindicta_core.gas_tank import GasTankState, CostEstimate

__all__ = [
    "VindictaModel", "TimestampedModel", "IdentifiableModel",
    "EntropyProof", "DiceResult", 
    "GasTankState", "CostEstimate",
]
```

#### [MODIFY] [interfaces.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/interfaces.py)

Refactor to re-export all symbols from new locations:

```python
"""Backward-compatible re-exports for vindicta_core.interfaces."""

from vindicta_core.dice import DiceEngineProtocol, BaseDiceEngine
from vindicta_core.gas_tank import GasTankProtocol, BaseGasTank
from vindicta_core.oracle import OracleProtocol

__all__ = [
    "DiceEngineProtocol", "BaseDiceEngine",
    "GasTankProtocol", "BaseGasTank",
    "OracleProtocol",
]
```

#### [MODIFY] [__init__.py](file:///c:/Users/bfoxt/.gemini/antigravity/playground/primordial-pulsar/Vindicta-Core/src/vindicta_core/__init__.py)

Update package exports to include new subpackages.

---

## File Structure After Refactoring

```
src/vindicta_core/
├── __init__.py          # Package root with version
├── models.py            # Backward-compat re-exports
├── interfaces.py        # Backward-compat re-exports
├── settings.py          # Unchanged
├── base/
│   └── __init__.py      # VindictaModel, TimestampedModel, IdentifiableModel
├── dice/
│   └── __init__.py      # EntropyProof, DiceResult, DiceEngineProtocol, BaseDiceEngine
├── gas_tank/
│   └── __init__.py      # GasTankState, CostEstimate, GasTankProtocol, BaseGasTank
└── oracle/
    └── __init__.py      # OracleProtocol
```

---

## Verification Plan

### Automated Tests

1. **Existing Test Suite (29 tests)**
   ```powershell
   cd Vindicta-Core
   uv run pytest tests/ -v
   ```
   - **Expected Result:** All 29 tests pass without modification
   - **Purpose:** Validates backward compatibility of import paths

2. **Import Path Verification Script**
   ```powershell
   uv run python -c "from vindicta_core.models import GasTankState, CostEstimate, DiceResult, EntropyProof, VindictaModel, TimestampedModel, IdentifiableModel; print('models.py imports OK')"
   uv run python -c "from vindicta_core.interfaces import DiceEngineProtocol, BaseDiceEngine, GasTankProtocol, BaseGasTank, OracleProtocol; print('interfaces.py imports OK')"
   ```
   - **Expected Result:** Both commands print success message
   - **Purpose:** Confirms backward-compat shims work correctly

3. **New Import Path Verification**
   ```powershell
   uv run python -c "from vindicta_core.base import VindictaModel; from vindicta_core.dice import DiceResult; from vindicta_core.gas_tank import GasTankState; from vindicta_core.oracle import OracleProtocol; print('New domain imports OK')"
   ```
   - **Expected Result:** Prints success message
   - **Purpose:** Confirms new domain-specific imports work

4. **Circular Import Check**
   ```powershell
   uv run python -c "import vindicta_core; print('No circular imports')"
   ```
   - **Expected Result:** Prints success without import errors

### Manual Verification

After implementation, user should:
1. Reinstall package: `uv pip install -e .` in Vindicta-Core directory
2. Verify installation: `uv pip show vindicta-core`
3. Confirm all consumers (Vindicta-API, etc.) still import successfully

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Circular imports | Low | High | Strict dependency rule enforced |
| Test failures | Low | High | Run tests before PR |
| Downstream breaks | Very Low | Medium | Backward-compat shims |
