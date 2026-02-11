from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://bizbot:bizbot_dev_password@localhost:5432/bizbot"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    MAGIC_LINK_SECRET: str = "dev-magic-link-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    MAGIC_LINK_EXPIRE_MINUTES: int = 15
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_NUMBER: Optional[str] = None
    
    # ElevenLabs
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # App
    PROJECT_NAME: str = "Biz-Bot"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
