import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Decentrathon Backend")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    token_ttl_minutes: int = int(os.getenv("TOKEN_TTL_MINUTES", "60"))


settings = Settings()

