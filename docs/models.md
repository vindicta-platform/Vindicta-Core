# Domain Models Reference

This document describes the core Pydantic models used throughout the Vindicta Platform.

## Model Hierarchy

```
VindictaModel (base)
└── TimestampedModel (adds created_at, updated_at)
    └── IdentifiableModel (adds UUID id)
```

## Base Models

### VindictaModel

Base model for all Vindicta entities. Provides JSON serialization support.

```python
from vindicta_core.models import VindictaModel

class MyModel(VindictaModel):
    name: str
```

### TimestampedModel

Adds automatic `created_at` and optional `updated_at` timestamps.

### IdentifiableModel

Adds auto-generated UUID `id` field. Use for entities that need unique identification.

---

## Dice & Entropy Models

Per **Constitution VI** (On Randomness), all dice rolls must be cryptographically verifiable.

### EntropyProof

Proof of entropy for dice rolls.

| Field | Type | Description |
|-------|------|-------------|
| `seed_hash` | str | SHA-256 of the entropy seed (required) |
| `timestamp` | datetime | When the proof was generated |
| `algorithm` | Literal | `"csprng"` or `"rejection_sampling"` |
| `audit_trail_id` | UUID | Unique identifier for audit trail |

**Example:**
```python
from vindicta_core.models import EntropyProof

proof = EntropyProof(seed_hash="abc123def456")
```

### DiceResult

Result of a dice roll with mandatory entropy proof.

| Field | Type | Description |
|-------|------|-------------|
| `value` | int | Rolled value (≥1, ≤sides) |
| `sides` | int | Number of sides on die (≥2) |
| `proof` | EntropyProof | Required entropy proof |

**Validation:** The `value` cannot exceed `sides`.

**Example:**
```python
from vindicta_core.models import DiceResult, EntropyProof

proof = EntropyProof(seed_hash="test")
result = DiceResult(value=4, sides=6, proof=proof)
```

---

## Gas Tank Models

Per **Constitution II** (On the Gas Tank), all premium features require balance checks.

### GasTankState

Represents current state of a user's gas tank.

| Field | Type | Description |
|-------|------|-------------|
| `balance_usd` | float | Current balance (≥0) |
| `limit_usd` | float | Maximum allowed spend |
| `is_active` | bool | Whether tank is active |

**Properties:**
- `is_empty`: True when balance is zero
- `is_low`: True when balance < 10% of limit

### CostEstimate

Cost estimate before executing a premium feature.

| Field | Type | Description |
|-------|------|-------------|
| `estimated_usd` | float | Estimated cost (≥0) |
| `feature_name` | str | Name of the feature |
| `can_proceed` | bool | Whether operation can proceed |
| `reason` | str | Explanation if cannot proceed |

**Example:**
```python
from vindicta_core.models import CostEstimate, GasTankState

tank = GasTankState(balance_usd=5.0, is_active=True)
estimate = CostEstimate(estimated_usd=0.50, feature_name="oracle_query")
result = estimate.evaluate_against_tank(tank)

if result.can_proceed:
    # Execute the feature
    pass
```

---

## Serialization

All models support JSON serialization via Pydantic:

```python
# Serialize to JSON
json_str = model.model_dump_json()

# Deserialize from JSON
restored = MyModel.model_validate_json(json_str)

# Get JSON schema
schema = MyModel.model_json_schema()
```
