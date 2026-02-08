# Implementation Plan: Wargame Domain Models (v0.1.0)

**Spec Reference:** [spec.md](./spec.md)
**Feature ID:** 003-domain-models
**Milestone:** v0.1.0 — Domain Models

---

## Goal

Add a `vindicta_core.wargame` subpackage containing 10 Pydantic v2 models
that represent the core concepts of competitive tabletop wargaming. These
models will be the canonical data structures consumed by WARScribe-Core,
Primordia-AI, Meta-Oracle, Vindicta-API, and Vindicta-Portal.

---

## Technical Context

### Existing Structure

```
src/vindicta_core/
├── __init__.py          # Re-exports all public symbols
├── models.py            # Infrastructure models (VindictaModel, DiceResult, etc.)
├── interfaces.py        # Protocols (DiceEngineProtocol, etc.)
├── settings.py          # Environment config
```

### Target Structure After This Feature

```
src/vindicta_core/
├── __init__.py          # Updated: adds wargame re-exports
├── models.py            # Unchanged (infrastructure models)
├── interfaces.py        # Unchanged
├── settings.py          # Unchanged
└── wargame/             # NEW
    ├── __init__.py      # Re-exports all wargame models
    ├── common.py        # Phase enum, StatsBlock, WeaponProfile, Ability
    ├── units.py         # Unit model
    ├── army.py          # ArmyList model
    ├── state.py         # UnitState, PlayerState, GameState (frozen)
    └── actions.py       # MoveAction, ShootAction, ChargeAction, FightAction, Action union
```

### Dependencies

- **Pydantic v2**: Already in `pyproject.toml`
- **Standard Library**: `uuid`, `datetime`, `enum`, `typing`
- **Internal**: Extends `VindictaModel` and `IdentifiableModel` from `models.py`

---

## Proposed Changes

### Wargame Package — Core Models

#### [NEW] wargame/__init__.py

Re-export all public symbols from submodules:

```python
from vindicta_core.wargame.common import Phase, StatsBlock, WeaponProfile, Ability
from vindicta_core.wargame.units import Unit
from vindicta_core.wargame.army import ArmyList
from vindicta_core.wargame.state import UnitState, PlayerState, GameState
from vindicta_core.wargame.actions import (
    MoveAction, ShootAction, ChargeAction, FightAction, Action,
)

__all__ = [
    "Phase", "StatsBlock", "WeaponProfile", "Ability",
    "Unit", "ArmyList",
    "UnitState", "PlayerState", "GameState",
    "MoveAction", "ShootAction", "ChargeAction", "FightAction", "Action",
]
```

---

#### [NEW] wargame/common.py

Contains shared primitives used by multiple wargame models:

- `Phase(str, Enum)` — 5 game phases in order
- `StatsBlock(VindictaModel)` — M/T/Sv/W/Ld/OC + optional invulnerable
- `WeaponProfile(VindictaModel)` — Weapon stats with dice expressions
- `Ability(VindictaModel)` — Rule ability with phase attachment

**Design decisions:**

- `Phase` extends `str` for JSON serialization friendliness.
- `WeaponProfile.attacks` and `.damage` are `str` to support dice expressions
  like `"D6+1"`. Parsing/evaluation is deferred to Dice-Engine integration.
- `StatsBlock` validates `save` range (2-7) and `invulnerable_save` (2-6).

---

#### [NEW] wargame/units.py

Contains the `Unit` model:

- Extends `IdentifiableModel` (gets UUID id, timestamps)
- Composition of `StatsBlock`, `list[WeaponProfile]`, `list[Ability]`
- `frozenset[str]` for keywords (hashable, immutable)
- Validators: `keywords` must have ≥ 1 entry, `name` non-empty

---

#### [NEW] wargame/army.py

Contains the `ArmyList` model:

- Extends `IdentifiableModel`
- Computed property `total_points` sums unit costs
- Model validator enforces `total_points <= points_limit`
- Contains player metadata (name, faction, detachment)

---

#### [NEW] wargame/state.py

Contains game state models:

- `UnitState(VindictaModel)` — Status tracking for a single unit
- `PlayerState(VindictaModel)` — CP/VP tracking + army reference
- `GameState(VindictaModel)` — **Frozen** (ConfigDict frozen=True)
  - Turn number, active player, active phase
  - Unit states dict, player states dict, objectives dict
  - Validator: exactly 2 players

**Design decisions:**

- `GameState` is frozen to support Primordia MCTS tree branching.
- New states created via `model_copy(update={...})` pattern.
- `UnitState.position` is `tuple[float, float] | None` for board coordinates.

---

#### [NEW] wargame/actions.py

Contains action models as a discriminated union:

- Base fields shared via a `_BaseAction(VindictaModel)` (frozen)
- `MoveAction`, `ShootAction`, `ChargeAction`, `FightAction` subclasses
- Type discrimination via `Literal["move"]`, `Literal["shoot"]`, etc.
- `Action = Annotated[MoveAction | ShootAction | ..., Discriminator("type")]`

---

### Package Integration

#### [MODIFY] __init__.py

Add wargame model re-exports to the package root:

```python
# Add to existing imports:
from vindicta_core.wargame import (
    Phase, StatsBlock, WeaponProfile, Ability,
    Unit, ArmyList,
    UnitState, PlayerState, GameState,
    MoveAction, ShootAction, ChargeAction, FightAction, Action,
)

# Add to __all__:
"Phase", "StatsBlock", "WeaponProfile", "Ability",
"Unit", "ArmyList",
"UnitState", "PlayerState", "GameState",
"MoveAction", "ShootAction", "ChargeAction", "FightAction", "Action",
```

---

### Tests

#### [NEW] tests/test_wargame_models.py

Comprehensive tests covering:

1. **StatsBlock validation** — Valid creation, out-of-range rejects
2. **WeaponProfile** — Melee (range=0) vs ranged, dice expressions
3. **Unit creation** — Happy path, empty keywords rejection
4. **ArmyList** — Points validation (under/over limit)
5. **Phase ordering** — Iteration yields correct sequence
6. **GameState immutability** — Mutation raises TypeError
7. **GameState copy** — `model_copy(update={})` creates new state
8. **Action discrimination** — JSON round-trip preserves type field
9. **Serialization round-trip** — All 10 models: model → JSON → model
10. **Player count validation** — GameState rejects != 2 players

#### [NEW] tests/test_wargame_serialization.py

Performance benchmark tests:

1. **2000pt army serialization** — < 5ms for typical game state
2. **Large game state** — Round-trip fidelity with max units

---

## Data Model Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         GameState (frozen)                      │
│  game_id, turn_number, active_player, active_phase             │
│                                                                 │
│  players: dict[str, PlayerState]                               │
│    ├── player_id, command_points, victory_points               │
│    └── army_list: ArmyList                                     │
│          ├── faction, detachment, points_limit                 │
│          └── units: list[Unit]                                 │
│                ├── name, stats: StatsBlock                     │
│                ├── keywords, faction_keywords                  │
│                ├── weapons: list[WeaponProfile]                │
│                └── abilities: list[Ability]                    │
│                                                                 │
│  unit_states: dict[UUID, UnitState]                            │
│    └── status, wounds_remaining, models_remaining, position    │
│                                                                 │
│  objectives: dict[str, str | None]                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Action (discriminated union)                │
│  MoveAction | ShootAction | ChargeAction | FightAction         │
│  Common: action_id, source_unit_id, turn, phase, timestamp     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Verification Plan

### Automated Tests

```powershell
# 1. Run all tests (existing + new)
cd Vindicta-Core
uv run pytest tests/ -v --tb=short

# 2. Type checking
uv run mypy src/vindicta_core/wargame/ --strict

# 3. Import verification
uv run python -c "from vindicta_core.wargame import Unit, GameState, Action, Phase; print('Wargame imports OK')"

# 4. Backward compat (existing imports still work)
uv run python -c "from vindicta_core.models import VindictaModel, DiceResult; print('Legacy imports OK')"

# 5. Serialization round-trip
uv run python -c "
from vindicta_core.wargame import Unit, StatsBlock
u = Unit(name='Intercessors', stats=StatsBlock(movement=6, toughness=4, save=3, wounds=2, leadership=6, oc=2), keywords=frozenset({'INFANTRY','PRIMARIS'}), faction_keywords=frozenset({'ADEPTUS ASTARTES'}), points_cost=80, model_count=5)
j = u.model_dump_json()
u2 = Unit.model_validate_json(j)
assert u == u2
print('Round-trip OK')
"
```

### Manual Verification

- Review model fields match 10th Edition core rules index
- Confirm downstream repos can import `vindicta_core.wargame` after install
