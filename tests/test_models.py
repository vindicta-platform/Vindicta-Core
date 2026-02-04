"""Tests for Vindicta Core models - Constitution XV compliant."""

import pytest
from uuid import UUID

from vindicta_core.models import (
    CostEstimate,
    DiceResult,
    EntropyProof,
    GasTankState,
    IdentifiableModel,
    VindictaModel,
)


class TestEntropyProof:
    """Tests for EntropyProof per Constitution VI."""
    
    def test_creates_with_required_fields(self):
        """EntropyProof requires seed_hash."""
        proof = EntropyProof(seed_hash="abc123")
        assert proof.seed_hash == "abc123"
        assert proof.algorithm == "csprng"
        assert isinstance(proof.audit_trail_id, UUID)
    
    def test_algorithm_options(self):
        """Supports csprng and rejection_sampling."""
        proof = EntropyProof(
            seed_hash="def456",
            algorithm="rejection_sampling"
        )
        assert proof.algorithm == "rejection_sampling"


class TestDiceResult:
    """Tests for DiceResult per Constitution VI."""
    
    def test_creates_with_proof(self):
        """DiceResult must include EntropyProof."""
        proof = EntropyProof(seed_hash="test")
        result = DiceResult(value=4, sides=6, proof=proof)
        
        assert result.value == 4
        assert result.sides == 6
        assert result.proof.seed_hash == "test"
    
    def test_value_must_be_positive(self):
        """Dice value must be >= 1."""
        proof = EntropyProof(seed_hash="test")
        with pytest.raises(ValueError):
            DiceResult(value=0, sides=6, proof=proof)


class TestGasTankState:
    """Tests for GasTankState per Constitution II."""
    
    def test_defaults_to_zero_balance(self):
        """Default balance is 0 (free tier)."""
        state = GasTankState()
        assert state.balance_usd == 0.0
        assert state.is_empty is True
    
    def test_is_empty_when_zero(self):
        """Tank is empty at zero balance."""
        state = GasTankState(balance_usd=0.0)
        assert state.is_empty is True
        
    def test_not_empty_with_balance(self):
        """Tank not empty with positive balance."""
        state = GasTankState(balance_usd=1.0)
        assert state.is_empty is False


class TestCostEstimate:
    """Tests for CostEstimate per Constitution II."""
    
    def test_requires_feature_name(self):
        """Estimate must specify feature."""
        estimate = CostEstimate(
            estimated_usd=0.01,
            feature_name="oracle_query"
        )
        assert estimate.feature_name == "oracle_query"
        assert estimate.can_proceed is False


class TestIdentifiableModel:
    """Tests for IdentifiableModel."""
    
    def test_auto_generates_uuid(self):
        """ID is auto-generated."""
        model = IdentifiableModel()
        assert isinstance(model.id, UUID)
    
    def test_has_timestamps(self):
        """Inherits timestamp fields."""
        model = IdentifiableModel()
        assert model.created_at is not None
