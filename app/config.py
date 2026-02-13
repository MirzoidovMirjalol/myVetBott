"""
Configuration settings for the bot
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Bot Configuration
    BOT_TOKEN: str
    BOT_NAME: str = "PetHelperBot"
    
    # Database Configuration
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    # Redis Configuration
    REDIS_URL: Optional[str] = None
    REDIS_DB: int = 0
    
    # Application Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Webhook Settings (optional, for production)
    WEBHOOK_ENABLED: bool = False
    WEBHOOK_URL: Optional[str] = None
    WEBHOOK_PATH: Optional[str] = "/webhook"
    WEBHOOK_HOST: str = "0.0.0.0"
    WEBHOOK_PORT: int = 8000
    
    # Security
    ALLOWED_UPDATES: list = ["message", "callback_query"]
    
    # Features
    ENABLE_SENTRY: bool = False
    SENTRY_DSN: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()
