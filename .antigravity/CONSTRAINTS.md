# Vindicta-Core Constraints

> Critical rules agents MUST follow when modifying this repository.

## ⛔ Hard Constraints

1. **Single Source of Truth** - All domain models originate here
2. **No External Dependencies** - Core has zero platform dependencies
3. **Pydantic v2 Only** - All schemas use Pydantic v2 syntax
4. **Immutable by Default** - Models should be frozen unless mutation required

## 📐 Schema Rules

### Naming Conventions
- Models: `PascalCase` (e.g., `ArmyList`, `MatchResult`)
- Fields: `snake_case` (e.g., `player_id`, `total_points`)
- Enums: `SCREAMING_SNAKE_CASE` values

### Required Fields
All models MUST include:
- `id: UUID` - Unique identifier
- `created_at: datetime` - Creation timestamp
- `version: int` - Schema version for migrations

### Validation
- Use `@field_validator` for business logic
- Use `@model_validator` for cross-field validation
- Never raise generic exceptions; use custom `ValidationError`

## 🔒 Compatibility Rules

- Breaking changes require version bump in all consumers
- Deprecated fields must be marked with `deprecated=True`
- New optional fields safe; new required fields are breaking

## 🧪 Testing Requirements

Before merging:
- [ ] `pytest` passes with 100% coverage on models
- [ ] All validators have positive and negative test cases
- [ ] Schema migration tests pass
