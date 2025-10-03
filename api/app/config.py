from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Server Configuration
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"

    # CORS
    ALLOWED_ORIGINS: str = "*"

    # Provider API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GROK_API_KEY: Optional[str] = None

    # AWS (for Bedrock)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
