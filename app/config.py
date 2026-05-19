from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROD : bool = False
    PROD_ENGINE_URI : str = ''
    TEST_SQLITE_FILE_NAME : str = "testdb.sqlite"
    TEST_ENGINE_URI : str = f"sqlite+pysqlite:///{TEST_SQLITE_FILE_NAME}"
    DEBUG : bool = True


settings = Settings()