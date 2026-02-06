# ADR-001: Python as Primary Language

**Status**: Accepted
**Date**: 2026-02-01

## Context

This repository requires a programming language for implementation. The choice affects developer experience, ecosystem compatibility, and maintenance burden.

## Decision

We adopt **Python 3.10+** as the primary language.

## Rationale

- **Ecosystem Alignment** — Vindicta Platform is Python-first
- **Tooling** — Rich ecosystem (pytest, ruff, mypy)
- **Async Support** — Native async/await for I/O operations
- **Type Safety** — Full type hints with Pydantic

## Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| TypeScript | Strong types, web-native | Different ecosystem, adds complexity | Rejected |
| Rust | Performance, safety | Higher learning curve, slower iteration | Rejected |
| Go | Concurrency, simple | Less expressive, limited ecosystem | Rejected |

## Consequences

- All source code in `src/` uses Python 3.10+
- Type hints required on all public APIs
- Ruff for linting/formatting
