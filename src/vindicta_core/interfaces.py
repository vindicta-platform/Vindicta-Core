"""Interface contracts for Vindicta Platform services.

Constitution Compliance:
- III. Spec-Driven: Interfaces define contracts before implementation
- XVI. Async-First: All interfaces use async signatures
"""

from abc import ABC, abstractmethod
from typing import Protocol

from vindicta_core.models import CostEstimate, DiceResult, GasTankState


class DiceEngineProtocol(Protocol):
    """Protocol for dice rolling services per Constitution VI.
    
    All implementations MUST:
    - Use CSPRNG for randomness
    - Generate EntropyProof for every roll
    - Apply rejection sampling to eliminate modulo bias
    """
    
    async def roll(self, sides: int, count: int = 1) -> list[DiceResult]:
        """Roll dice with cryptographic randomness."""
        ...
    
    async def roll_d6(self, count: int = 1) -> list[DiceResult]:
        """Roll standard d6 dice (Warhammer 40K standard)."""
        ...


class GasTankProtocol(Protocol):
    """Protocol for Gas Tank cost control per Constitution II.
    
    All cost-incurring features MUST:
    - Estimate cost before execution
    - Check Gas Tank balance
    - STOP immediately when tank is empty
    """
    
    async def get_state(self) -> GasTankState:
        """Get current Gas Tank state."""
        ...
    
    async def estimate_cost(self, feature: str, **kwargs) -> CostEstimate:
        """Estimate cost before igniting a feature."""
        ...
    
    async def consume(self, amount_usd: float, feature: str) -> bool:
        """Consume gas for a feature. Returns False if insufficient."""
        ...


class OracleProtocol(Protocol):
    """Protocol for AI Oracle services per Constitution II.
    
    MUST use Gemini models via Vertex AI or AI Studio.
    """
    
    async def query(self, prompt: str, context: dict | None = None) -> str:
        """Query the Oracle with a prompt."""
        ...
    
    async def estimate_tokens(self, prompt: str) -> int:
        """Estimate token count for a prompt."""
        ...


# Abstract base classes for implementations

class BaseDiceEngine(ABC):
    """Abstract base for dice engine implementations."""
    
    @abstractmethod
    async def roll(self, sides: int, count: int = 1) -> list[DiceResult]:
        """Roll dice with cryptographic randomness."""
        pass
    
    async def roll_d6(self, count: int = 1) -> list[DiceResult]:
        """Roll standard d6."""
        return await self.roll(6, count)
    
    async def roll_d3(self, count: int = 1) -> list[DiceResult]:
        """Roll d3 (half d6, rounded up)."""
        d6_results = await self.roll(6, count)
        return [
            DiceResult(
                value=(r.value + 1) // 2,
                sides=3,
                proof=r.proof
            )
            for r in d6_results
        ]


class BaseGasTank(ABC):
    """Abstract base for Gas Tank implementations."""
    
    @abstractmethod
    async def get_state(self) -> GasTankState:
        """Get current state."""
        pass
    
    @abstractmethod
    async def estimate_cost(self, feature: str, **kwargs) -> CostEstimate:
        """Estimate feature cost."""
        pass
    
    @abstractmethod
    async def consume(self, amount_usd: float, feature: str) -> bool:
        """Consume gas. Returns False if empty."""
        pass
