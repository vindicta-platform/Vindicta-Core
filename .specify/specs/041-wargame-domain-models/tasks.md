# Tasks: Wargame Domain Models

**Feature Branch**: `041-wargame-domain-models`
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)
**Created**: 2026-02-08

---

## User Story: US-05 — API Consumer Foundation

> All models must inherit from VindictaModel and be JSON-serializable

### T-001: Create wargame subpackage scaffold

- **Priority**: P0 (foundation)
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/__init__.py`
- **Acceptance Criteria**:
  - [ ] Create `src/vindicta_core/wargame/` directory
  - [ ] Create `__init__.py` with `__all__` export list (initially empty)
  - [ ] Verify package importable: `from vindicta_core.wargame import *`
- **Dependencies**: None

### T-002: Create Phase enum and TurnPhase model

- **Priority**: P0 (leaf dependency)
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/phase.py`
- **Acceptance Criteria**:
  - [ ] `Phase` StrEnum with values: command, movement, shooting, charge, fight, morale
  - [ ] `TurnPhase` model with `turn_number` (ge=1), `phase`, `active_player`
  - [ ] All values serialize as lowercase strings
- **Dependencies**: T-001

---

## User Story: US-02 — Meta-Oracle Agent

> ArmyList models with points, faction, and keyword data

### T-003: Create UnitProfile model

- **Priority**: P0
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/unit.py`
- **Acceptance Criteria**:
  - [ ] `UnitProfile(VindictaModel)` with fields: movement (str), toughness (int), save (int, 2-7), wounds (int, ge=1), leadership (int), objective_control (int, ge=0)
  - [ ] Field validators for stat ranges
- **Dependencies**: T-001

### T-004: Create Weapon model

- **Priority**: P0
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/unit.py`
- **Acceptance Criteria**:
  - [ ] `Weapon(VindictaModel)` with fields: name, range (str), attacks (str), skill (int), strength (int), armor_penetration (int), damage (str), keywords (list[str])
  - [ ] String fields for variable values (attacks="D6", damage="D3")
  - [ ] Keywords as list of uppercase strings
- **Dependencies**: T-001

### T-005: Create Unit model

- **Priority**: P0
- **Estimate**: 20 min
- **File**: `src/vindicta_core/wargame/unit.py`
- **Acceptance Criteria**:
  - [ ] `Unit(IdentifiableModel)` with: name, faction, keywords, profile (UnitProfile), weapons (list[Weapon]), abilities (list[str]), points_cost (int, ge=0), models_count (int, ge=1), models_remaining (int, ge=0)
  - [ ] Validator: `models_remaining <= models_count`
  - [ ] UUID auto-generated, timestamps from parent
- **Dependencies**: T-003, T-004

### T-006: Create ArmyList model

- **Priority**: P0
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/army.py`
- **Acceptance Criteria**:
  - [ ] `ArmyList(IdentifiableModel)` with: name, faction, subfaction (optional), units (list[Unit]), total_points, points_limit (default 2000), edition (default "10th")
  - [ ] `validate_points(limit: int | None = None) -> bool` method
  - [ ] Empty units list is valid
- **Dependencies**: T-005

---

## User Story: US-03 — Game Tracker

> Action models with phase context and timestamps

### T-007: Create base Action model

- **Priority**: P1
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `Action(IdentifiableModel)` with: action_type (str, discriminator), phase (Phase), acting_unit_id (UUID), timestamp (datetime)
  - [ ] Configured for discriminated union pattern
- **Dependencies**: T-002

### T-008: Create MoveAction

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `MoveAction(Action)` with: action_type="move", distance (str)
  - [ ] Phase must be MOVEMENT
- **Dependencies**: T-007

### T-009: Create ShootAction

- **Priority**: P1
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `ShootAction(Action)` with: action_type="shoot", target_unit_id (UUID), weapon_name (str), hit_rolls (list[DiceResult]), wound_rolls (list[DiceResult]), saves_failed (int, ge=0), damage_dealt (int, ge=0)
  - [ ] Phase must be SHOOTING
  - [ ] DiceResult imported from vindicta_core.models
- **Dependencies**: T-007

### T-010: Create ChargeAction

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `ChargeAction(Action)` with: action_type="charge", target_unit_id (UUID), charge_roll (DiceResult | None), successful (bool)
  - [ ] Phase must be CHARGE
- **Dependencies**: T-007

### T-011: Create FightAction

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `FightAction(Action)` with: action_type="fight", target_unit_id (UUID), weapon_name (str), hit_rolls, wound_rolls, saves_failed, damage_dealt
  - [ ] Phase must be FIGHT
- **Dependencies**: T-007

### T-012: Create ActionUnion discriminated type

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/actions.py`
- **Acceptance Criteria**:
  - [ ] `ActionUnion = Annotated[Union[MoveAction, ShootAction, ChargeAction, FightAction], Field(discriminator='action_type')]`
  - [ ] JSON deserialization correctly dispatches to subclass
- **Dependencies**: T-008, T-009, T-010, T-011

---

## User Story: US-01 — AI Engine Developer

> Frozen GameState snapshots for MCTS

### T-013: Create PlayerState model

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/game.py`
- **Acceptance Criteria**:
  - [ ] `PlayerState(VindictaModel)` with: player_id (UUID), army_list (ArmyList), command_points (int, ge=0), victory_points (int, ge=0), secondary_points (int, ge=0)
- **Dependencies**: T-006

### T-014: Create GameState model

- **Priority**: P1
- **Estimate**: 20 min
- **File**: `src/vindicta_core/wargame/game.py`
- **Acceptance Criteria**:
  - [ ] `GameState(IdentifiableModel)` with: player_a (PlayerState), player_b (PlayerState), current_phase (Phase), current_turn (int, ge=1), current_player (Literal["A","B"]), actions (list[ActionUnion]), is_complete (bool)
  - [ ] Mutable by default (`model_config = ConfigDict(frozen=False)`)
- **Dependencies**: T-012, T-013

### T-015: Implement GameState.freeze()

- **Priority**: P1
- **Estimate**: 15 min
- **File**: `src/vindicta_core/wargame/game.py`
- **Acceptance Criteria**:
  - [ ] `FrozenGameState(GameState)` with `model_config = ConfigDict(frozen=True)`
  - [ ] `GameState.freeze() -> FrozenGameState` creates deep-frozen copy
  - [ ] Assignment to frozen state raises `ValidationError`
  - [ ] Frozen instances are hashable
- **Dependencies**: T-014

---

## User Story: US-04 — Battle Transcript Toolkit

> Wargame package exports for downstream

### T-016: Update wargame `__init__.py` exports

- **Priority**: P1
- **Estimate**: 10 min
- **File**: `src/vindicta_core/wargame/__init__.py`
- **Acceptance Criteria**:
  - [ ] Export all public models in `__all__`
  - [ ] Import paths: `from vindicta_core.wargame import Unit, ArmyList, GameState, Phase, ...`
- **Dependencies**: T-002 through T-015

### T-017: Update vindicta_core `__init__.py`

- **Priority**: P2
- **Estimate**: 5 min
- **File**: `src/vindicta_core/__init__.py`
- **Acceptance Criteria**:
  - [ ] Add `wargame` to package exports
  - [ ] `from vindicta_core import wargame` works
- **Dependencies**: T-016

---

## User Story: Cross-cutting — Quality Gates

### T-018: Unit tests for all wargame models

- **Priority**: P0 (gate for merge)
- **Estimate**: 45 min
- **File**: `tests/test_wargame_models.py`
- **Acceptance Criteria**:
  - [ ] All models can be instantiated with valid data
  - [ ] All validators reject invalid data
  - [ ] Edge cases: empty lists, zero points, max values
  - [ ] Models_remaining <= models_count enforced
- **Dependencies**: T-016

### T-019: JSON serialization round-trip tests

- **Priority**: P0 (gate for merge)
- **Estimate**: 30 min
- **File**: `tests/test_wargame_serialization.py`
- **Acceptance Criteria**:
  - [ ] All models survive `model_dump(mode='json')` → `Model(**data)` round-trip
  - [ ] UUID fields serialize as strings
  - [ ] Phase enum serializes as string
  - [ ] ActionUnion deserializes to correct subclass
  - [ ] `model_json_schema()` produces valid JSON Schema
- **Dependencies**: T-016

### T-020: Freeze / immutability tests

- **Priority**: P1
- **Estimate**: 20 min
- **File**: `tests/test_wargame_freeze.py`
- **Acceptance Criteria**:
  - [ ] `GameState.freeze()` returns `FrozenGameState`
  - [ ] Assignment to frozen state raises `ValidationError`
  - [ ] Original remains mutable after freeze
  - [ ] Frozen copy is independent (mutation doesn't propagate)
- **Dependencies**: T-015

### T-021: Mypy strict mode verification

- **Priority**: P0 (gate for merge)
- **Estimate**: 15 min
- **Acceptance Criteria**:
  - [ ] `uv run mypy src/vindicta_core/wargame/ --strict` passes with zero errors
  - [ ] All public functions have type annotations
  - [ ] No `Any` types used
- **Dependencies**: T-016

### T-022: Coverage gate

- **Priority**: P0 (gate for merge)
- **Estimate**: 10 min
- **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_wargame*.py --cov=vindicta_core.wargame` >= 90%
  - [ ] All branches exercised
- **Dependencies**: T-018, T-019, T-020

---

## Dependency Graph

```
T-001 (scaffold)
  ├── T-002 (Phase)
  │     └── T-007 (Action base)
  │           ├── T-008 (MoveAction)
  │           ├── T-009 (ShootAction)
  │           ├── T-010 (ChargeAction)
  │           └── T-011 (FightAction)
  │                 └── T-012 (ActionUnion)
  ├── T-003 (UnitProfile)
  ├── T-004 (Weapon)
  │     └── T-005 (Unit)
  │           └── T-006 (ArmyList)
  │                 └── T-013 (PlayerState)
  │                       └── T-014 (GameState)
  │                             └── T-015 (freeze)
  └── T-016 (exports) ← depends on all above
        ├── T-017 (root exports)
        ├── T-018 (tests)
        ├── T-019 (serialization tests)
        └── T-020 (freeze tests)
              ├── T-021 (mypy)
              └── T-022 (coverage)
```

## Parallelization Opportunities

| Parallel Group | Tasks                      | Rationale                   |
| -------------- | -------------------------- | --------------------------- |
| Group A        | T-002, T-003, T-004        | Independent leaf models     |
| Group B        | T-008, T-009, T-010, T-011 | Independent action subtypes |
| Group C        | T-018, T-019, T-020        | Independent test files      |

---

## Summary

| Metric         | Value    |
| -------------- | -------- |
| Total tasks    | 22       |
| P0 tasks       | 10       |
| P1 tasks       | 10       |
| P2 tasks       | 2        |
| New files      | 10       |
| Modified files | 1        |
| Estimated time | ~5 hours |
