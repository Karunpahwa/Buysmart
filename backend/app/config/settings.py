from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # OLX Scraping
    olx_base_url: str = "https://www.olx.in"
    scraper_delay: int = 2
    max_concurrent_scrapes: int = 5
    
    # App Settings
    debug: bool = True
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 