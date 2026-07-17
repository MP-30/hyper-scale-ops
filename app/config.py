import os
from pydantic import Field
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE = os.getenv("ENV_FILE", ".env")
if not os.path.isabs(ENV_FILE):
    ENV_FILE = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", ENV_FILE)
    )

VAULT_FILE = Path("/vault/secrets/config")

if VAULT_FILE.exists():
    with VAULT_FILE.open() as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            # Don't overwrite existing environment variables
            os.environ.setdefault(key, value)

class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    app_port: int = 8000
    debug_mode: bool = False

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()
