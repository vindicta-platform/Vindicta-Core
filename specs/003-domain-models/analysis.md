# Analysis Report: 003-domain-models

**Feature:** Wargame Domain Models (v0.1.0)
**Artifacts Analyzed:** spec.md, plan.md
**Analysis Date:** 2026-02-08
**Status:** PASS ✅

---

## Summary

All specification artifacts are internally consistent and aligned with
the project constitution and roadmap. No CRITICAL issues found. Two
MINOR observations noted for awareness.

---

## Detection Results

### ✅ Duplication Check — PASS

No duplicate requirements found between spec.md and plan.md.
The spec defines WHAT; the plan defines HOW. Clear separation.

### ✅ Ambiguity Check — PASS

All three original ambiguities (Edition Handling, ID Strategy, Immutability)
are resolved in Section 6 of the spec with clear rationale.

### ✅ Underspecification Check — PASS

All 10 models have complete field definitions with types and constraints.
Action union discrimination strategy is explicit.

### ✅ Constitution Alignment — PASS

| Principle                | Status | Notes                                  |
| ------------------------ | ------ | -------------------------------------- |
| VII. Mechanical Fidelity | ✅      | Models match 10th Ed stat lines        |
| XVI. Async-First         | ✅      | All models serialization-ready         |
| II. Gas Tank             | N/A    | Not applicable to domain models        |
| VI. Entropy              | N/A    | Dice models already exist in models.py |

### ✅ Coverage Check — PASS

| Roadmap Deliverable                     | Spec Coverage   | Plan Coverage      |
| --------------------------------------- | --------------- | ------------------ |
| Unit model (stats, abilities, keywords) | US-01, §4.1-4.4 | wargame/units.py   |
| Army list model                         | US-04, §4.5     | wargame/army.py    |
| Game state model                        | US-02, §4.7-4.9 | wargame/state.py   |
| Action model (move, shoot, fight)       | US-03, §4.10    | wargame/actions.py |
| Phase/turn model                        | US-05, §4.6     | wargame/common.py  |

### ✅ Consistency Check — PASS

- Field types in spec tables match plan code snippets.
- Model hierarchy (VindictaModel → IdentifiableModel → Unit) is consistent.
- Test coverage plan maps 1:1 to models defined in spec.

---

## Minor Observations

### OBS-01: Dice Expression Parsing (MINOR)

**Observation:** `WeaponProfile.attacks` and `.damage` use `str` type for
dice expressions ("D6+1", "D3"). No parser is defined in this spec.

**Assessment:** Acceptable. Spec §7 (Out of Scope) explicitly defers dice
expression evaluation to Dice-Engine integration. The string type is correct
for v0.1.0 data modeling.

**Action Required:** None for this spec. Future spec needed for dice parsing.

### OBS-02: Board Geometry (MINOR)

**Observation:** `UnitState.position` uses `tuple[float, float]` but board
dimensions, terrain, and measurement rules are out of scope.

**Assessment:** Acceptable. The position field enables basic tracking. Full
geometry is a separate feature (likely v0.2.0+).

**Action Required:** None for this spec.

---

## Cross-Reference Matrix

| Spec Section       | Plan File          | Test Coverage               |
| ------------------ | ------------------ | --------------------------- |
| §4.1 WeaponProfile | wargame/common.py  | test_wargame_models #2      |
| §4.2 Ability       | wargame/common.py  | Included in unit tests      |
| §4.3 StatsBlock    | wargame/common.py  | test_wargame_models #1      |
| §4.4 Unit          | wargame/units.py   | test_wargame_models #3      |
| §4.5 ArmyList      | wargame/army.py    | test_wargame_models #4      |
| §4.6 Phase         | wargame/common.py  | test_wargame_models #5      |
| §4.7 PlayerState   | wargame/state.py   | Included in GameState tests |
| §4.8 UnitState     | wargame/state.py   | Included in GameState tests |
| §4.9 GameState     | wargame/state.py   | test_wargame_models #6,7,10 |
| §4.10 Actions      | wargame/actions.py | test_wargame_models #8      |
| §5 NFRs            | All files          | test_wargame_serialization  |

---

## Verdict

**PROCEED TO IMPLEMENTATION** — All artifacts are consistent, complete,
and aligned with both the roadmap deliverables and the project constitution.
