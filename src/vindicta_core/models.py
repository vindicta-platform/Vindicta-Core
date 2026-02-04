"""Base models for Vindicta Platform.

Constitution Compliance:
- VII. Mechanical Fidelity: Models support 40K 10th Ed mechanics
- XVI. Async-First: All models are serialization-ready
"""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class VindictaModel(BaseModel):
    """Base model for all Vindicta entities.
    
    Provides common fields and serialization behavior.
    """
    
    class Config:
        frozen = False
        populate_by_name = True
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }


class TimestampedModel(VindictaModel):
    """Model with automatic timestamps."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


class IdentifiableModel(TimestampedModel):
    """Model with UUID identifier."""
    
    id: UUID = Field(default_factory=uuid4)


# Dice & Randomness (Constitution VI)

class EntropyProof(VindictaModel):
    """Proof of entropy for dice rolls per Constitution VI.
    
    Every mechanical event MUST generate a traceable EntropyProof.
    """
    
    seed_hash: str = Field(..., description="SHA-256 of the entropy seed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    algorithm: Literal["csprng", "rejection_sampling"] = "csprng"
    audit_trail_id: UUID = Field(default_factory=uuid4)


class DiceResult(VindictaModel):
    """Result of a dice roll with entropy proof."""
    
    value: int = Field(..., ge=1, description="Rolled value")
    sides: int = Field(..., ge=2, description="Number of sides on die")
    proof: EntropyProof


# Gas Tank (Constitution II)

class GasTankState(VindictaModel):
    """Current state of the Gas Tank per Constitution II."""
    
    balance_usd: float = Field(0.0, ge=0.0)
    limit_usd: float = Field(0.0, ge=0.0, description="Max allowed spend")
    is_active: bool = True
    
    @property
    def is_empty(self) -> bool:
        """Gas Tank is empty when balance reaches zero."""
        return self.balance_usd <= 0.0


class CostEstimate(VindictaModel):
    """Cost estimate before igniting a Gas Tank feature."""
    
    estimated_usd: float = Field(..., ge=0.0)
    feature_name: str
    can_proceed: bool = False
    reason: str | None = None
