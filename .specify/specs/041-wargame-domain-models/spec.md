# Feature Specification: Wargame Domain Models

**Feature Branch**: `041-wargame-domain-models`
**Created**: 2026-02-08
**Status**: Draft
**Target**: Week 2 | **Repository**: Vindicta-Core
**Milestone**: v0.1.0 — Domain Models
**Feature ID**: CORE-041
**Priority**: P0

---

## 1. Problem Statement

The Vindicta Platform currently has **infrastructure-level domain models** (VindictaModel, DiceResult, GasTankState, CostEstimate) but **zero wargame-specific models**. Every downstream product — Primordia-AI, Meta-Oracle, WARScribe-Core, Logi-Slate-UI, Battle-Transcript-Toolkit — needs a shared vocabulary for:

- **Units**: The fundamental game entity with stats, abilities, and weapons
- **Army Lists**: Collections of units belonging to a faction
- **Game State**: The complete board state at any point in a game
- **Actions**: Discrete game events (move, shoot, charge, fight)
- **Phases/Turns**: The sequencing structure of a game round

Without these shared models, each product will invent its own incompatible representations, making cross-product integration impossible.

---

## 2. Vision

Establish the **canonical wargame domain language** for the Vindicta Platform by creating a set of Pydantic v2 models that:

- Serve as the **single source of truth** for all products
- Are **edition-agnostic** (support 10th Edition now, extensible to future editions)
- Are **immutable where needed** for AI consumption (Primordia-AI requires frozen state snapshots)
- Are **JSON-serializable** with full round-trip fidelity for API transport
- Carry **entropy proofs** on all dice-dependent actions (Constitution VI compliance)

---

## 3. User Stories

### US-01: AI Engine Developer (Primordia-AI)

> As a **Primordia-AI developer**,
> I want **frozen GameState snapshots** with all unit stats resolved,
> So that **MCTS search can evaluate positions without mutation side effects**.

**Acceptance Criteria:**

- [ ] `GameState` model has a `frozen=True` config option
- [ ] All nested models (units, scores) are immutable when frozen
- [ ] `GameState.hash()` produces deterministic hashes for identical states
- [ ] Deep copy creates an independent snapshot

### US-02: Meta-Oracle Agent

> As a **Meta-Oracle agent**,
> I want **ArmyList models with points, faction, and keyword data**,
> So that **I can evaluate list composition quality and predict matchup outcomes**.

**Acceptance Criteria:**

- [ ] `ArmyList` contains total points, faction keyword, and unit list
- [ ] Each `Unit` exposes keywords, abilities, and points cost
- [ ] `ArmyList.validate_points(limit)` checks legality
- [ ] Faction keywords are normalized strings

### US-03: Game Tracker (Logi-Slate-UI)

> As a **Logi-Slate-UI game tracker**,
> I want **Action models with phase context and timestamps**,
> So that **I can record game events in real-time with <30 sec entry time**.

**Acceptance Criteria:**

- [ ] `Action` model captures: acting unit, target, phase, result, timestamp
- [ ] Action subtypes: `MoveAction`, `ShootAction`, `ChargeAction`, `FightAction`
- [ ] Each action type has phase-appropriate fields (e.g., ShootAction has wound rolls)
- [ ] Serializes to compact JSON for local storage

### US-04: Battle Transcript Toolkit

> As a **Battle-Transcript-Toolkit developer**,
> I want **GameEvent wrappers around Actions with causality chains**,
> So that **I can reconstruct a complete game narrative from event logs**.

**Acceptance Criteria:**

- [ ] Actions can be composed into ordered event sequences
- [ ] Events carry sequential IDs and parent references
- [ ] A game can be reconstructed from its action log
- [ ] Action logs serialize to WARScribe-compatible JSON

### US-05: API Consumer (Vindicta-API)

> As the **Vindicta-API**,
> I want **all models to be JSON-serializable with OpenAPI-compatible schemas**,
> So that **FastAPI can auto-generate endpoint schemas from these models**.

**Acceptance Criteria:**

- [ ] All models inherit from `VindictaModel` (Pydantic BaseModel)
- [ ] `model_json_schema()` produces valid JSON Schema
- [ ] UUID fields serialize as strings
- [ ] Enum fields serialize as string values
- [ ] Nested models serialize cleanly (no circular references)

---

## 4. Proposed Models

### 4.1 Unit Model

```python
class UnitProfile(VindictaModel):
    """Stat profile for a wargame unit."""
    movement: str          # e.g., "6\""
    toughness: int
    save: int              # armor save value (2-7, 7 = no save)
    wounds: int
    leadership: int
    objective_control: int

class Weapon(VindictaModel):
    """A weapon profile attached to a unit."""
    name: str
    range: str             # e.g., "24\"" or "Melee"
    attacks: str           # e.g., "3" or "D6"
    skill: int             # ballistic or weapon skill
    strength: int
    armor_penetration: int
    damage: str            # e.g., "1" or "D3"
    keywords: list[str]    # e.g., ["RAPID FIRE 1", "ANTI-INFANTRY 4+"]

class Unit(IdentifiableModel):
    """A single game unit with its datasheet profile."""
    name: str
    faction: str
    keywords: list[str]          # e.g., ["INFANTRY", "IMPERIUM", "INTERCESSORS"]
    profile: UnitProfile
    weapons: list[Weapon]
    abilities: list[str]
    points_cost: int
    models_count: int            # number of models in the unit
    models_remaining: int        # for tracking casualties
```

### 4.2 ArmyList Model

```python
class ArmyList(IdentifiableModel):
    """A complete army list for a game."""
    name: str
    faction: str
    subfaction: str | None = None  # e.g., detachment
    units: list[Unit]
    total_points: int
    points_limit: int = 2000
    edition: str = "10th"
```

### 4.3 GameState Model

```python
class PlayerState(VindictaModel):
    """State for one player in a game."""
    player_id: UUID
    army_list: ArmyList
    command_points: int = 0
    victory_points: int = 0
    secondary_points: int = 0

class GameState(IdentifiableModel):
    """Complete game state at a point in time."""
    player_a: PlayerState
    player_b: PlayerState
    current_phase: Phase
    current_turn: int = 1
    current_player: Literal["A", "B"]
    actions: list[Action] = []
    is_complete: bool = False
```

### 4.4 Phase/Turn Enums

```python
class Phase(str, Enum):
    COMMAND = "command"
    MOVEMENT = "movement"
    SHOOTING = "shooting"
    CHARGE = "charge"
    FIGHT = "fight"
    MORALE = "morale"  # not in 10e but reserved

class TurnPhase(VindictaModel):
    """A specific phase within a turn."""
    turn_number: int
    phase: Phase
    active_player: Literal["A", "B"]
```

### 4.5 Action Models

```python
class Action(IdentifiableModel):
    """Base action in a wargame turn."""
    action_type: str            # discriminator
    phase: Phase
    acting_unit_id: UUID
    timestamp: datetime

class MoveAction(Action):
    action_type: Literal["move"] = "move"
    distance: str               # e.g., "6\""

class ShootAction(Action):
    action_type: Literal["shoot"] = "shoot"
    target_unit_id: UUID
    weapon_name: str
    hit_rolls: list[DiceResult] = []
    wound_rolls: list[DiceResult] = []
    saves_failed: int = 0
    damage_dealt: int = 0

class ChargeAction(Action):
    action_type: Literal["charge"] = "charge"
    target_unit_id: UUID
    charge_roll: DiceResult | None = None
    successful: bool = False

class FightAction(Action):
    action_type: Literal["fight"] = "fight"
    target_unit_id: UUID
    weapon_name: str
    hit_rolls: list[DiceResult] = []
    wound_rolls: list[DiceResult] = []
    saves_failed: int = 0
    damage_dealt: int = 0
```

---

## 5. Non-Goals

- **Rules engine**: No game rule enforcement or validation (that's WARScribe-Core)
- **Persistence layer**: No database ORM; models are pure data containers
- **UI rendering**: No display logic; models are consumed by UI layers
- **Edition-specific logic**: No hardcoded 10th Ed rules; edition metadata only
- **AI evaluation**: No heuristic logic; models are data for AI consumption

---

## 6. Constraints

| Constraint                                        | Source                    |
| ------------------------------------------------- | ------------------------- |
| Pydantic v2 with `model_config` (not v1 `Config`) | Tech stack                |
| `frozen=True` for AI-consumed snapshots           | Primordia-AI requirement  |
| JSON-serializable with full round-trip            | API transport requirement |
| UUID identifiers (not int autoincrement)          | Constitution XVI          |
| Entropy proofs on all dice-dependent actions      | Constitution VI           |
| Zero new external dependencies beyond Pydantic    | Constitution III          |
| Mypy strict mode compliance                       | Quality Gate              |
| 90%+ test coverage on all models                  | Roadmap KR                |

---

## 7. Open Questions

1. ~~Should `Phase` include `MORALE` for forward-compat with 11th Edition?~~ **Yes** — include as reserved enum value
2. ~~Should `Unit.models_remaining` track individual model wounds?~~ **No** — track at unit level only for v0.1.0; per-model wound tracking deferred
3. ~~Should `Action` use discriminated unions (`Annotated[Union[...], Field(discriminator='action_type')]`)?~~ **Yes** — enables clean JSON deserialization
4. ~~Should `GameState` be frozen by default or opt-in?~~ **Opt-in** — mutable by default, frozen snapshot via `.freeze()` method

---

## 8. Clarification Cycle 1: Ambiguity Search

### Identified Ambiguities

| Term               | Ambiguity                                                              | Resolution                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Edition-agnostic" | How to handle edition-specific stats (e.g., OC doesn't exist pre-10th) | **Resolution**: `UnitProfile` fields represent 10th Ed stats. Future editions extend `UnitProfile` via subclass. `edition` field on `ArmyList` tags the data source. |
| "Immutable for AI" | Full frozen graph or selective?                                        | **Resolution**: `GameState` gets a `.freeze()` method returning a deep-frozen copy. Normal usage is mutable.                                                         |
| "Points cost"      | Per-model or per-unit?                                                 | **Resolution**: Per-unit (full unit cost). Per-model cost not tracked in v0.1.0.                                                                                     |
| "Keywords"         | Faction keywords vs ability keywords?                                  | **Resolution**: Single `keywords: list[str]` field. Convention: UPPERCASE for faction keywords (e.g., "IMPERIUM"), Title Case for abilities.                         |
| "Weapon attacks"   | String vs int (some weapons are "D6")                                  | **Resolution**: `str` type to handle variable attacks like "2D6", "D3+1". Parsing is WARScribe-Core's responsibility.                                                |

### Decisions Made

1. **UUID Strategy**: All identifiable models use UUIDv4 via `uuid4()` default factory
2. **Timestamp Strategy**: Use `datetime.utcnow` factory (matches existing `TimestampedModel`)
3. **Serialization**: Standard Pydantic v2 `.model_dump(mode='json')` — no custom serializers needed
4. **Discriminated Unions**: Use `Annotated[Union[MoveAction, ShootAction, ...], Field(discriminator='action_type')]` for polymorphic action lists

---

## 9. Clarification Cycle 2: Component Impact

### Files Requiring Modification

| File                                    | Change Type | Impact                                                           |
| --------------------------------------- | ----------- | ---------------------------------------------------------------- |
| `src/vindicta_core/wargame/__init__.py` | **NEW**     | New subpackage for all wargame models                            |
| `src/vindicta_core/wargame/unit.py`     | **NEW**     | UnitProfile, Weapon, Unit models                                 |
| `src/vindicta_core/wargame/army.py`     | **NEW**     | ArmyList model                                                   |
| `src/vindicta_core/wargame/game.py`     | **NEW**     | PlayerState, GameState models                                    |
| `src/vindicta_core/wargame/phase.py`    | **NEW**     | Phase enum, TurnPhase model                                      |
| `src/vindicta_core/wargame/actions.py`  | **NEW**     | Action base + MoveAction, ShootAction, ChargeAction, FightAction |
| `src/vindicta_core/__init__.py`         | **MODIFY**  | Add wargame exports                                              |
| `tests/test_wargame_models.py`          | **NEW**     | Full test suite for all wargame models                           |
| `tests/test_wargame_serialization.py`   | **NEW**     | JSON round-trip tests                                            |
| `tests/test_wargame_freeze.py`          | **NEW**     | Immutability tests for AI consumption                            |

### Downstream Consumer Impact

| Consumer                  | Integration Point                                       | Required Action                |
| ------------------------- | ------------------------------------------------------- | ------------------------------ |
| Primordia-AI              | `from vindicta_core.wargame import GameState, Unit`     | Blueprint for state encoding   |
| Meta-Oracle               | `from vindicta_core.wargame import ArmyList, Unit`      | Blueprint for list grading     |
| WARScribe-Core            | `from vindicta_core.wargame import Unit, Weapon, Phase` | Data target for parsed rosters |
| Logi-Slate-UI             | `from vindicta_core.wargame import Action, GameState`   | Event recording format         |
| Battle-Transcript-Toolkit | `from vindicta_core.wargame import Action`              | Event extraction target        |
| Vindicta-API              | All models                                              | API schema generation          |

---

## 10. Clarification Cycle 3: Edge Case / Failure Analysis

### Potential Failure Modes

| Scenario                                         | Risk       | Mitigation                                                                                                                        |
| ------------------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Circular import between wargame and dice modules | **MEDIUM** | `Action` imports `DiceResult` (one-way). wargame → dice is OK; dice must never import wargame.                                    |
| UUID collision across distributed clients        | **LOW**    | UUIDv4 has negligible collision probability. Not a concern for v0.1.0.                                                            |
| GameState too large for JSON transport           | **MEDIUM** | Full game state with all actions could be large. Mitigate: actions stored separately, GameState holds only current snapshot.      |
| Weapon.attacks string parsing errors             | **MEDIUM** | Parsing is WARScribe-Core's problem. Models store raw strings. Include `Weapon.attacks_display()` for human-readable format only. |
| Frozen GameState mutation attempt                | **LOW**    | Pydantic `frozen=True` raises `ValidationError` on assignment. Well-documented behavior.                                          |

### Edge Cases

1. **Empty army list**: `ArmyList(units=[])` — valid state (army building in progress)
2. **Zero-point unit**: `Unit(points_cost=0)` — valid (some units are free)
3. **Unit with no weapons**: Valid (some units are purely support)
4. **Game with only 1 player**: Not valid — `GameState` requires both `player_a` and `player_b`
5. **Action without dice results**: Valid — `MoveAction` has no dice. `ShootAction` with empty `hit_rolls` means no shots taken.
6. **Turn 0**: Not valid — turns start at 1 (`current_turn: int = 1, ge=1`)

---

## 11. Quality Checklist

- [x] Problem statement clearly defines the gap
- [x] Vision connects to platform-wide architecture
- [x] User stories cover all major consumers
- [x] Acceptance criteria are testable
- [x] Non-goals explicitly stated
- [x] Constraints reference Constitution and tech stack
- [x] Open questions resolved
- [x] 3 clarification cycles completed (ambiguity, impact, edge cases)
- [x] No TBD or placeholder content remains
