from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Itinerary API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # Add more as needed

    model_config = ConfigDict(env_file=".env")


settings = Settings()
