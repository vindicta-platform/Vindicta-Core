# Setup Guide

## Prerequisites
- Python 3.10+
- uv

## Development Setup
```bash
git clone https://github.com/vindicta-platform/Vindicta-Core.git
cd Vindicta-Core
uv venv
uv pip install -e ".[dev]"
```

## Running Tests
```powershell
pytest tests/ -v
```
