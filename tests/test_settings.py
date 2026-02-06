"""Tests for Vindicta Core Settings - Constitution XV compliant."""

from vindicta_core.settings import Settings


def test_settings_defaults():
    """Settings have correct defaults per Constitution I."""
    # Arrange/Act
    settings = Settings()

    # Assert - Constitution I: GCP project locked
    assert settings.gcp_project == "vindicta-warhammer"
    assert settings.gas_tank_limit_usd == 0.0  # Free tier only


def test_settings_gemini_default():
    """Gemini model configured per Constitution II."""
    # Arrange/Act
    settings = Settings()

    # Assert
    assert "gemini" in settings.gemini_model.lower()


def test_settings_async_enabled():
    """Async I/O enabled by default per Constitution XVI."""
    # Arrange/Act
    settings = Settings()

    # Assert
    assert settings.async_io_enabled is True
