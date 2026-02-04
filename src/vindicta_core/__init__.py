"""Vindicta Core - Shared primitives and settings.

Constitution XVI compliant: Async-ready configuration.
"""

from vindicta_core.interfaces import (
    BaseDiceEngine,
    BaseGasTank,
    DiceEngineProtocol,
    GasTankProtocol,
    OracleProtocol,
)
from vindicta_core.models import (
    CostEstimate,
    DiceResult,
    EntropyProof,
    GasTankState,
    IdentifiableModel,
    TimestampedModel,
    VindictaModel,
)
from vindicta_core.settings import Settings

__all__ = [
    # Settings
    "Settings",
    # Models
    "VindictaModel",
    "TimestampedModel",
    "IdentifiableModel",
    "EntropyProof",
    "DiceResult",
    "GasTankState",
    "CostEstimate",
    # Interfaces
    "DiceEngineProtocol",
    "GasTankProtocol",
    "OracleProtocol",
    "BaseDiceEngine",
    "BaseGasTank",
]
