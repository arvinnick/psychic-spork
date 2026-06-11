import os.path as path
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = BASE_DIR.parent
class Settings(BaseSettings):
    PROD : bool = False
    PROD_ENGINE_URI : str = ''
    DEV_SQLITE_FILE_NAME : str = f"{BASE_DIR}/devdb.sqlite"
    DEV_ENGINE_URI : str = f"sqlite+aiosqlite:///{DEV_SQLITE_FILE_NAME}"
    TEST_SQLITE_FILE_NAME: str = f"{BASE_DIR}/testdb.sqlite"
    TEST_ENGINE_URI: str = f"sqlite+aiosqlite:///{TEST_SQLITE_FILE_NAME}"
    DEBUG : bool = False
    echo_sql: bool = True
    HASH_SALT : str
    HASH_MIN_LEN: int



settings = Settings(_env_file=f"{PARENT_DIR}{path.sep}.env")
