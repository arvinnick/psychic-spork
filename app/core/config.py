from os import environ
from pathlib import Path
from pydantic_settings import BaseSettings

from app.core import logger

BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = BASE_DIR.parent
POSTGRES_USER = environ["POSTGRES_USER"]
POSTGRES_PASSWORD = environ["POSTGRES_PASSWORD"]
POSTGRES_DB = environ["POSTGRES_DB"]
logger.logger.info(f"Postgres database: {POSTGRES_DB}")
class Settings(BaseSettings):
    PROD : bool = False
    PROD_ENGINE_URI : str = ''
    DEV_ENGINE_URI : str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@dev_db:5432/{POSTGRES_DB}"
    TEST_SQLITE_FILE_NAME: str = f"{BASE_DIR}/testdb.sqlite"
    TEST_ENGINE_URI: str = f"sqlite+aiosqlite:///{TEST_SQLITE_FILE_NAME}"
    DEBUG : bool = True
    ECHO_SQL: bool = False
    HASH_SALT : str | None = None
    HASH_MIN_LEN: int | None = None



settings = Settings()
if settings.DEBUG:
    logger.logger.info(f"settings: {dict(settings)}")