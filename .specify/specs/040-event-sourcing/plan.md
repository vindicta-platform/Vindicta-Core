# Implementation Plan: Event Sourcing Primitives

**Branch**: `040-event-sourcing` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)

## Summary

Event sourcing foundation with immutable event storage and replay. Supports state reconstruction from event streams.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Pydantic, SQLite
**Storage**: SQLite (append-only)
**Testing**: pytest
**Target Platform**: Vindicta-Core
**Project Type**: Backend library

## Project Structure

```text
Vindicta-Core/src/
└── events/
    ├── store.py             # [NEW] Event store
    ├── models.py            # [NEW] Event models
    └── replay.py            # [NEW] Replay logic
```
