"""Base models for Vindicta Platform.

Constitution Compliance:
- VII. Mechanical Fidelity: Models support 40K 10th Ed mechanics
- XVI. Async-First: All models are serialization-ready
"""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


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
    
    @field_validator('seed_hash')
    @classmethod
    def seed_hash_not_empty(cls, v: str) -> str:
        """Seed hash must not be empty."""
        if not v or not v.strip():
            raise ValueError('seed_hash cannot be empty')
        return v


class DiceResult(VindictaModel):
    """Result of a dice roll with entropy proof."""
    
    value: int = Field(..., ge=1, description="Rolled value")
    sides: int = Field(..., ge=2, description="Number of sides on die")
    proof: EntropyProof
    
    @model_validator(mode='after')
    def value_within_sides(self) -> 'DiceResult':
        """Validate that rolled value does not exceed die sides."""
        if self.value > self.sides:
            raise ValueError(
                f'value ({self.value}) cannot exceed sides ({self.sides})'
            )
        return self


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
    
    @property
    def is_low(self) -> bool:
        """Gas Tank is low when balance is below 10% of limit."""
        if self.limit_usd <= 0:
            return self.balance_usd <= 0.0
        return self.balance_usd < (self.limit_usd * 0.1)


class CostEstimate(VindictaModel):
    """Cost estimate before igniting a Gas Tank feature."""
    
    estimated_usd: float = Field(..., ge=0.0)
    feature_name: str
    can_proceed: bool = False
    reason: str | None = None
    
    @field_validator('feature_name')
    @classmethod
    def feature_name_not_empty(cls, v: str) -> str:
        """Feature name must not be empty."""
        if not v or not v.strip():
            raise ValueError('feature_name cannot be empty')
        return v
    
    def evaluate_against_tank(self, tank: GasTankState) -> 'CostEstimate':
        """Evaluate if this cost can proceed against a gas tank state.
        
        Returns a new CostEstimate with can_proceed and reason set.
        """
        if not tank.is_active:
            return CostEstimate(
                estimated_usd=self.estimated_usd,
                feature_name=self.feature_name,
                can_proceed=False,
                reason="Gas tank is inactive"
            )
        if tank.balance_usd < self.estimated_usd:
            return CostEstimate(
                estimated_usd=self.estimated_usd,
                feature_name=self.feature_name,
                can_proceed=False,
                reason=f"Insufficient balance: {tank.balance_usd:.2f} < {self.estimated_usd:.2f}"
            )
        return CostEstimate(
            estimated_usd=self.estimated_usd,
            feature_name=self.feature_name,
            can_proceed=True,
            reason=None
        )
