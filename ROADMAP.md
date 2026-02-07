# Vindicta-Core Roadmap

> **Vision**: Shared domain models and business logic for the platform
> **Status**: Foundation
> **Last Updated**: 2026-02-03

---

## v1.0 Target: March 2026

### Mission Statement
Provide the canonical domain models, shared utilities, and core business logic that all Vindicta products depend on.

---

## Milestone Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│  Feb 2026          Mar 2026          Apr 2026                   │
│  ─────────────────────────────────────────────────────────────  │
│  [v0.1.0]          [v0.2.0]          [v1.0.0]                   │
│  Domain Models     Refactor          Stable                     │
│                                                                  │
│  Week 1-2          Week 3-4          Week 5+                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## v0.1.0 — Domain Models (Target: Feb 10, 2026)

### Deliverables
- [ ] Unit model (stats, abilities, keywords)
- [ ] Army list model
- [ ] Game state model
- [ ] Action model (move, shoot, fight)
- [ ] Phase/turn model

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Model Coverage** | All core concepts | Code review |
| **Type Safety** | 100% typed | mypy strict |
| **Documentation** | All models documented | Doc coverage |

### Exit Criteria
- [ ] Core models defined
- [ ] Used by WARScribe-Core
- [ ] Published to PyPI (private)

---

## v0.2.0 — Refactor & Extract (Target: Feb 24, 2026)

### Deliverables
- [ ] Extract WARScribe module to WARScribe-Core
- [ ] Extract Meta-Oracle module to Meta-Oracle
- [ ] Clean up dependencies
- [ ] Standardize error handling
- [ ] Async-first patterns

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Module Extraction** | 2 modules extracted | Code review |
| **Dependency Graph** | No circular deps | tooling check |
| **Async Coverage** | All I/O is async | Code review |

### Exit Criteria
- [ ] WARScribe-Core standalone
- [ ] Meta-Oracle standalone
- [ ] Core package slim and focused

---

## v1.0.0 — Stable Release (Target: Mar 15, 2026)

### Deliverables
- [ ] Stable API
- [ ] Comprehensive test suite
- [ ] Performance benchmarks
- [ ] Migration guides for consumers
- [ ] PyPI publication

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Test Coverage** | >90% | pytest-cov |
| **API Stability** | No breaking changes | Semantic versioning |
| **Performance** | Benchmarks documented | Benchmark suite |

### Exit Criteria
- [ ] All dependent products using v1.0
- [ ] No breaking changes planned
- [ ] Documentation complete

---

## Core Modules

| Module | Description | Status |
|--------|-------------|--------|
| `models` | Domain models (Unit, List, Game) | ✅ Exists |
| `warscribe` | Game notation (→ WARScribe-Core) | 🔄 Extracting |
| `meta_oracle` | Meta analysis (→ Meta-Oracle) | 🔄 Extracting |
| `quota` | Quota management (→ Agent-Auditor) | 🔄 Extracting |
| `utils` | Shared utilities | ✅ Exists |

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Pydantic v2 | ✅ Available | Model validation |
| DuckDB | ✅ Available | Data storage |

---

## Consumers

All Vindicta products depend on Vindicta-Core:

- WARScribe-Core
- Meta-Oracle
- Primordia AI
- Agent-Auditor-SDK
- Vindicta-API
- Vindicta-Portal

---

## Success Criteria

1. **Stability**: No breaking changes after v1.0
2. **Adoption**: All products use Core models
3. **Performance**: No bottlenecks in shared code

---

*Maintained by: Vindicta Platform Team*
