from pathlib import Path
from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CAR_UPLOAD_URL: Path
    ICON_UPLOAD_URL: Path
    DATABASE_URL: str

    class Config:
        env_file = BASE_DIR / '.env'

settings = Settings()