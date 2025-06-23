from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_CONNECTION: str
    SECRET_KEY: str

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
