from pathlib import Path
from pydantic.v1 import BaseSettings

# Project root directory, used to locate the .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CAR_UPLOAD_URL: Path
    ICON_UPLOAD_URL: Path
    STATIC_URL: str
    TEMPLATES_URL: str
    DATABASE_URL: str

    class Config:
        env_file = BASE_DIR / '.env'

settings = Settings()