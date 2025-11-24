from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Casablanca Fear & Greed Index API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./fear_greed.db"
    timescale_enabled: bool = False
    scheduler_timezone: str = "Africa/Casablanca"
    scheduler_daily_run: str = "16:00"
    models_dir: Path = Path("./models")
    
    # Supabase Configuration (optionnel)
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_key: str | None = None
    
    # Redis Configuration (optionnel, fallback en mémoire si non configuré)
    redis_url: str | None = Field(default=None, description="Redis URL (ex: redis://localhost:6379/0)")
    
    # Security Configuration
    secret_key: str = Field(
        default="change-me-in-production-please-use-a-strong-random-secret-key",
        description="Secret key for JWT tokens (CHANGE IN PRODUCTION!)"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration in minutes")
    
    # OpenAI API Key (optionnel)
    openai_api_key: str | None = Field(default=None, description="OpenAI API key for LLM sentiment analysis")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_per_minute: int = Field(default=60, description="Requests per minute per IP")
    rate_limit_per_hour: int = Field(default=1000, description="Requests per hour per IP")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()