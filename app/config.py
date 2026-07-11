import os
from pydantic import Field
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env")
if not os.path.isabs(ENV_FILE):
    ENV_FILE = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", ENV_FILE)
    )

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
