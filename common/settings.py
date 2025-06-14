from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    DATABASE_URL: str     
    REDIS_BROKER_URL: str
    REDIS_RESULT_BACKEND: Optional[str]
    
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"


settings = Settings()
