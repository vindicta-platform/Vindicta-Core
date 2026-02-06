"""Vindicta Core Settings - Pydantic Settings for platform configuration.

Constitution Compliance:
- I. Economic Prime: GCP project locked to vindicta-warhammer
- XV. Quality Gates: Environment injection via fixtures only
- XVI. Async-First: Settings support async initialization
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Platform-wide configuration.

    All GCP operations MUST use the vindicta-warhammer project
    per Constitution I. Economic Prime Directive.
    """

    model_config = SettingsConfigDict(
        env_prefix="VINDICTA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # GCP Configuration (Constitution I)
    gcp_project: str = "vindicta-warhammer"
    gcp_region: str = "us-central1"

    # Gas Tank (Constitution II)
    gas_tank_enabled: bool = True
    gas_tank_limit_usd: float = 0.0  # Free tier only

    # AI Configuration (Constitution II)
    gemini_model: str = "gemini-1.5-flash"

    # Feature Flags
    debug: bool = False
    async_io_enabled: bool = True  # XVI compliance


# Singleton for import convenience
settings = Settings()
