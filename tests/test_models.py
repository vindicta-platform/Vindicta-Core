"""Tests for Vindicta Core models - Constitution XV compliant."""

import json
import pytest
from uuid import UUID

from vindicta_core.models import (
    CostEstimate,
    DiceResult,
    EntropyProof,
    GasTankState,
    IdentifiableModel,
    TimestampedModel,
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
    
    def test_seed_hash_cannot_be_empty(self):
        """Seed hash must not be empty."""
        with pytest.raises(ValueError, match="seed_hash cannot be empty"):
            EntropyProof(seed_hash="")
    
    def test_seed_hash_cannot_be_whitespace(self):
        """Seed hash must not be only whitespace."""
        with pytest.raises(ValueError, match="seed_hash cannot be empty"):
            EntropyProof(seed_hash="   ")


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
    
    def test_value_cannot_exceed_sides(self):
        """Dice value must not exceed number of sides."""
        proof = EntropyProof(seed_hash="test")
        with pytest.raises(ValueError, match="value.*cannot exceed sides"):
            DiceResult(value=7, sides=6, proof=proof)
    
    def test_value_can_equal_sides(self):
        """Dice value can equal max sides (e.g., rolling a 6 on d6)."""
        proof = EntropyProof(seed_hash="test")
        result = DiceResult(value=6, sides=6, proof=proof)
        assert result.value == 6


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
    
    def test_is_low_with_limit(self):
        """Tank is low when balance < 10% of limit."""
        state = GasTankState(balance_usd=0.5, limit_usd=10.0)
        assert state.is_low is True
    
    def test_not_low_with_sufficient_balance(self):
        """Tank is not low with sufficient balance."""
        state = GasTankState(balance_usd=2.0, limit_usd=10.0)
        assert state.is_low is False


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
    
    def test_feature_name_cannot_be_empty(self):
        """Feature name must not be empty."""
        with pytest.raises(ValueError, match="feature_name cannot be empty"):
            CostEstimate(estimated_usd=0.01, feature_name="")
    
    def test_evaluate_against_tank_success(self):
        """Can proceed when tank has sufficient balance."""
        tank = GasTankState(balance_usd=1.0, is_active=True)
        estimate = CostEstimate(estimated_usd=0.5, feature_name="test")
        result = estimate.evaluate_against_tank(tank)
        assert result.can_proceed is True
        assert result.reason is None
    
    def test_evaluate_against_tank_insufficient(self):
        """Cannot proceed when tank has insufficient balance."""
        tank = GasTankState(balance_usd=0.1, is_active=True)
        estimate = CostEstimate(estimated_usd=0.5, feature_name="test")
        result = estimate.evaluate_against_tank(tank)
        assert result.can_proceed is False
        assert "Insufficient balance" in result.reason
    
    def test_evaluate_against_inactive_tank(self):
        """Cannot proceed when tank is inactive."""
        tank = GasTankState(balance_usd=10.0, is_active=False)
        estimate = CostEstimate(estimated_usd=0.5, feature_name="test")
        result = estimate.evaluate_against_tank(tank)
        assert result.can_proceed is False
        assert "inactive" in result.reason


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


class TestModelSerialization:
    """Tests for JSON serialization per Constitution XVI."""
    
    def test_entropy_proof_round_trip(self):
        """EntropyProof serializes and deserializes correctly."""
        original = EntropyProof(seed_hash="test123")
        json_str = original.model_dump_json()
        restored = EntropyProof.model_validate_json(json_str)
        
        assert restored.seed_hash == original.seed_hash
        assert restored.algorithm == original.algorithm
        assert restored.audit_trail_id == original.audit_trail_id
    
    def test_dice_result_round_trip(self):
        """DiceResult serializes with nested proof."""
        proof = EntropyProof(seed_hash="nested")
        original = DiceResult(value=4, sides=6, proof=proof)
        json_str = original.model_dump_json()
        restored = DiceResult.model_validate_json(json_str)
        
        assert restored.value == original.value
        assert restored.sides == original.sides
        assert restored.proof.seed_hash == original.proof.seed_hash
    
    def test_gas_tank_state_json_schema(self):
        """GasTankState produces valid JSON schema."""
        schema = GasTankState.model_json_schema()
        assert "properties" in schema
        assert "balance_usd" in schema["properties"]
        assert "limit_usd" in schema["properties"]
    
    def test_cost_estimate_round_trip(self):
        """CostEstimate serializes correctly."""
        original = CostEstimate(
            estimated_usd=0.05,
            feature_name="oracle",
            can_proceed=True
        )
        json_str = original.model_dump_json()
        restored = CostEstimate.model_validate_json(json_str)
        
        assert restored.estimated_usd == original.estimated_usd
        assert restored.feature_name == original.feature_name
        assert restored.can_proceed == original.can_proceed
    
    def test_identifiable_model_uuid_serialization(self):
        """UUID serializes as string, deserializes back to UUID."""
        original = IdentifiableModel()
        data = original.model_dump()
        
        # UUID should be serializable to JSON
        json_str = json.dumps(data, default=str)
        assert str(original.id) in json_str
        
        # Restore from dict
        restored = IdentifiableModel.model_validate(data)
        assert restored.id == original.id
    
    def test_datetime_iso_format(self):
        """Timestamps serialize to ISO 8601 format."""
        model = TimestampedModel()
        data = model.model_dump()
        
        # created_at should be a datetime that can be serialized
        json_str = model.model_dump_json()
        parsed = json.loads(json_str)
        
        # ISO format includes 'T' separator
        assert "T" in parsed["created_at"]
