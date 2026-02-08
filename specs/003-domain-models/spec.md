# Specification: Wargame Domain Models (v0.1.0)

**Feature ID:** 003-domain-models
**Milestone:** v0.1.0 — Domain Models
**Priority:** P0 — Foundation
**Status:** Specified
**Target Date:** Feb 10, 2026

---

## 1. Problem Statement

The `vindicta_core` package currently defines infrastructure primitives
(VindictaModel, DiceResult, GasTankState) but lacks the actual **wargame
domain models** that every downstream product needs. Without canonical
representations of Units, Army Lists, Game States, Actions, and Phases,
each consumer (WARScribe-Core, Primordia-AI, Meta-Oracle, Vindicta-API,
Vindicta-Portal) will independently create incompatible models, causing
the integration fragmentation that this platform was designed to prevent.

---

## 2. Vision

Introduce a `vindicta_core.wargame` subpackage containing the foundational
domain models for competitive tabletop wargaming. These models become the
**shared language** for the entire Vindicta ecosystem.

---

## 3. User Stories

### US-01: WARScribe Developer — Unit Representation

> As a **WARScribe developer**,
> I want to **create a `Unit` from a parsed roster file**,
> So that **the notation engine can reference type-safe unit profiles**.

**Acceptance Criteria:**

- [ ] `Unit` model contains: name, stats block, keywords, wargear, abilities
- [ ] Stats block includes: M, T, Sv, W, Ld, OC as typed fields
- [ ] Keywords are a `frozenset[str]` for hashability
- [ ] Wargear items reference `WeaponProfile` models
- [ ] `Unit` is JSON-serializable via Pydantic `.model_dump_json()`

### US-02: Primordia AI — Game State Encoding

> As a **Primordia AI engineer**,
> I want to **serialize a complete GameState to JSON**,
> So that **the MCTS engine can evaluate board positions**.

**Acceptance Criteria:**

- [ ] `GameState` contains: turn number, active phase, active player, board state
- [ ] Board state is a mapping of unit IDs to `UnitState` (alive/destroyed/reserve)
- [ ] CP and VP tracked per player
- [ ] `GameState` is frozen (immutable) for safe use in search trees
- [ ] Serialization round-trip preserves all fields

### US-03: Meta-Oracle — Action Recording

> As a **Meta-Oracle agent**,
> I want to **record game actions** (move, shoot, charge, fight),
> So that **the debate engine can analyze move quality**.

**Acceptance Criteria:**

- [ ] All action types are union-discriminated via a `type` literal field
- [ ] Each action references source unit(s) and target unit(s) by ID
- [ ] `ShootAction` includes weapon profile and hit/wound roll results
- [ ] Actions are immutable after creation

### US-04: Tournament Organizer — List Validation

> As a **tournament organizer** using Vindicta-API,
> I want to **validate an army list** against point limits,
> So that **I can reject invalid submissions**.

**Acceptance Criteria:**

- [ ] `ArmyList` enforces a `points_limit` constraint
- [ ] Validation returns clear errors listing which units cause overflow
- [ ] `ArmyList` contains faction, detachment, player metadata

### US-05: Portal Developer — Phase Navigation

> As a **Vindicta-Portal developer**,
> I want to **render the current game phase and available actions**,
> So that **the UI can guide users through the turn sequence**.

**Acceptance Criteria:**

- [ ] `Phase` is an enum: Command, Movement, Shooting, Charge, Fight
- [ ] Phases are ordered and can be iterated in sequence
- [ ] `Turn` model composes player + phase sequence + turn number

---

## 4. Functional Requirements

### 4.1 WeaponProfile Model

| Field          | Type             | Constraints                                  |
| -------------- | ---------------- | -------------------------------------------- |
| `name`         | `str`            | Non-empty                                    |
| `range_inches` | `int`            | `>= 0` (0 = melee)                           |
| `attacks`      | `str`            | Dice expression or int (e.g., "D6+1", "3")   |
| `skill`        | `int`            | `2-6` (ballistic/weapon skill)               |
| `strength`     | `int`            | `>= 1`                                       |
| `ap`           | `int`            | `<= 0` (armor penetration, negative values)  |
| `damage`       | `str`            | Dice expression or int (e.g., "D3", "2")     |
| `keywords`     | `frozenset[str]` | Optional weapon keywords (RAPID FIRE, BLAST) |

### 4.2 Ability Model

| Field         | Type            | Constraints                                 |
| ------------- | --------------- | ------------------------------------------- |
| `id`          | `str`           | Unique identifier (slug format)             |
| `name`        | `str`           | Display name                                |
| `description` | `str`           | Rules text                                  |
| `phase`       | `Phase \| None` | Phase when ability applies (None = passive) |

### 4.3 StatsBlock Model

| Field               | Type          | Constraints                |
| ------------------- | ------------- | -------------------------- |
| `movement`          | `int`         | `>= 0` (inches)            |
| `toughness`         | `int`         | `>= 1`                     |
| `save`              | `int`         | `2-7` (2+ to no save)      |
| `wounds`            | `int`         | `>= 1`                     |
| `leadership`        | `int`         | `>= 1`                     |
| `oc`                | `int`         | `>= 0` (objective control) |
| `invulnerable_save` | `int \| None` | `2-6` or None              |

### 4.4 Unit Model

| Field              | Type                  | Constraints                       |
| ------------------ | --------------------- | --------------------------------- |
| `id`               | `UUID`                | Auto-generated                    |
| `name`             | `str`                 | Non-empty                         |
| `stats`            | `StatsBlock`          | Required                          |
| `keywords`         | `frozenset[str]`      | At least 1 keyword                |
| `faction_keywords` | `frozenset[str]`      | At least 1 faction keyword        |
| `weapons`          | `list[WeaponProfile]` | Can be empty                      |
| `abilities`        | `list[Ability]`       | Can be empty                      |
| `points_cost`      | `int`                 | `>= 0`                            |
| `model_count`      | `int`                 | `>= 1` (number of models in unit) |

### 4.5 ArmyList Model

| Field          | Type         | Constraints             |
| -------------- | ------------ | ----------------------- |
| `id`           | `UUID`       | Auto-generated          |
| `player_name`  | `str`        | Non-empty               |
| `faction`      | `str`        | Non-empty               |
| `detachment`   | `str`        | Non-empty               |
| `points_limit` | `int`        | `> 0`                   |
| `units`        | `list[Unit]` | At least 1              |
| `total_points` | computed     | Sum of unit points_cost |

Validation: `total_points <= points_limit` — raises `ValidationError` on failure.

### 4.6 Phase Enum

```python
class Phase(str, Enum):
    COMMAND = "command"
    MOVEMENT = "movement"
    SHOOTING = "shooting"
    CHARGE = "charge"
    FIGHT = "fight"
```

Ordered: iterating `Phase` yields phases in correct game order.

### 4.7 PlayerState Model

| Field            | Type       | Constraints |
| ---------------- | ---------- | ----------- |
| `player_id`      | `str`      | Non-empty   |
| `command_points` | `int`      | `>= 0`      |
| `victory_points` | `int`      | `>= 0`      |
| `army_list`      | `ArmyList` | Required    |

### 4.8 UnitState Model

| Field              | Type                                                    | Constraints                     |
| ------------------ | ------------------------------------------------------- | ------------------------------- |
| `unit_id`          | `UUID`                                                  | References a `Unit.id`          |
| `status`           | `Literal["active", "destroyed", "reserve", "embarked"]` | Required                        |
| `wounds_remaining` | `int`                                                   | `>= 0`                          |
| `models_remaining` | `int`                                                   | `>= 0`                          |
| `position`         | `tuple[float, float] \| None`                           | Board position (inches) or None |

### 4.9 GameState Model (Frozen)

| Field           | Type                     | Constraints                       |
| --------------- | ------------------------ | --------------------------------- |
| `game_id`       | `UUID`                   | Auto-generated                    |
| `turn_number`   | `int`                    | `>= 1`                            |
| `active_player` | `str`                    | Player ID                         |
| `active_phase`  | `Phase`                  | Current phase                     |
| `players`       | `dict[str, PlayerState]` | Exactly 2 players                 |
| `unit_states`   | `dict[UUID, UnitState]`  | All units from both armies        |
| `objectives`    | `dict[str, str \| None]` | Objective ID → controlling player |

Configuration: `model_config = ConfigDict(frozen=True)` — immutable for AI search.

### 4.10 Action Models (Discriminated Union)

Base action fields: `action_id: UUID`, `source_unit_id: UUID`, `turn: int`, `phase: Phase`, `timestamp: datetime`.

| Action Type    | Additional Fields                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------- |
| `MoveAction`   | `start_position: tuple`, `end_position: tuple`, `advance_roll: int \| None`                       |
| `ShootAction`  | `target_unit_id: UUID`, `weapon: WeaponProfile`, `hit_rolls: list[int]`, `wound_rolls: list[int]` |
| `ChargeAction` | `target_unit_ids: list[UUID]`, `charge_roll: tuple[int, int]`, `successful: bool`                 |
| `FightAction`  | `target_unit_id: UUID`, `weapon: WeaponProfile`, `hit_rolls: list[int]`, `wound_rolls: list[int]` |

Union: `Action = MoveAction | ShootAction | ChargeAction | FightAction`
Discrimination: field `type: Literal["move" | "shoot" | "charge" | "fight"]`

---

## 5. Non-Functional Requirements

| Category              | Requirement                                        |
| --------------------- | -------------------------------------------------- |
| **Type Safety**       | 100% strict mypy compliance                        |
| **Serialization**     | JSON round-trip < 5ms for 2000pt game              |
| **Immutability**      | `GameState` MUST be frozen; Actions MUST be frozen |
| **Python Version**    | 3.12+                                              |
| **Dependencies**      | Pydantic v2 only (no new deps)                     |
| **Schema Versioning** | Semantic versioning for model changes              |

---

## 6. Clarification Resolutions

| Question             | Resolution                                                                                                                      | Rationale                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Edition Handling** | Models target 10th Ed only for v0.1.0. Edition-agnostic abstraction deferred to WARScribe-Core v0.2.0 Edition Abstraction Layer | Prevents over-engineering; WARScribe layer handles edition polymorphism                                           |
| **ID Strategy**      | UUIDs for all entity IDs                                                                                                        | Required for distributed systems (multi-client sync), AI search tree deduplication, and cross-service referencing |
| **Immutability**     | Strict frozen models for `GameState` and all `Action` types. Mutable `UnitState` allowed during game state construction         | Primordia MCTS requires structural sharing; frozen models enable safe tree branching                              |

---

## 7. Out of Scope

- Game engine logic (resolving attacks, applying damage)
- Database ORM mapping
- UI components
- Edition abstraction (deferred to WARScribe-Core v0.2.0)
- Faction-specific abilities or stratagems
- Board geometry / terrain models

---

## 8. Constraints

- **Constitution VII (Mechanical Fidelity)**: Models MUST faithfully represent
  10th Edition game mechanics without approximation
- **Constitution XVI (Async-First)**: All models MUST be serialization-ready
- **No New Dependencies**: Only Pydantic v2 (already a dependency)
- **Backward Compatibility**: Existing models.py imports MUST continue working

---

## 9. Success Criteria

| Metric         | Target                                                                                               | Measurement Method |
| -------------- | ---------------------------------------------------------------------------------------------------- | ------------------ |
| Model coverage | 10 models (Weapon, Ability, Stats, Unit, ArmyList, Phase, PlayerState, UnitState, GameState, Action) | Code review        |
| Type safety    | Zero mypy errors                                                                                     | `mypy --strict`    |
| Test coverage  | > 90%                                                                                                | `pytest-cov`       |
| Serialization  | JSON round-trip < 5ms                                                                                | Benchmark script   |
| Docs           | All models in API reference                                                                          | `mkdocs build`     |
