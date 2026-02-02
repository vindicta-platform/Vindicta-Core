# ADR-002: Pre-commit Hooks Required

**Status**: Accepted  
**Date**: 2026-02-01

## Context

Code quality and consistency require enforcement before commits reach the repository.

## Decision

All repositories MUST configure **pre-commit** hooks.

## Required Hooks

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

## Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| CI-only | Simpler setup | Late feedback | Rejected |
| Husky (JS) | Popular | Different ecosystem | Rejected |
| Manual | Zero config | Inconsistent | Rejected |

## Consequences

- `.pre-commit-config.yaml` required in all repos
- Developers must run `pre-commit install` after clone
- CI will also run pre-commit as verification
