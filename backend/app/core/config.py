from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://bizbot:bizbot_dev_password@localhost:5432/bizbot"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    # WARNING: Generate secure secrets for production using: openssl rand -hex 32
    SECRET_KEY: str = "dev_secret_key_CHANGE_IN_PRODUCTION_using_openssl_rand"
    MAGIC_LINK_SECRET: str = "dev_magic_link_secret_CHANGE_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MAGIC_LINK_EXPIRE_MINUTES: int = 15
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    TWILIO_WHATSAPP_NUMBER: Optional[str] = None
    
    # ElevenLabs
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
