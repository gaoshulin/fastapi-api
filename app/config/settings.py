from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI MVC Project"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A complete FastAPI project with MVC architecture"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    API_PREFIX: str = "/api/v1"
    
    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASS: str = ""
    
    # DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_URL: str = "mysql+pymysql://root:ServBay.dev@localhost:3306/galen_test?charset=utf8mb4"

    SECRET_KEY: str = "ABk4judennbIeXJkB2DZN8n3zAQcEqH7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()