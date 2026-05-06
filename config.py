from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    PROD: bool = False
    PROD_ENGINE_URI: str = model_config.PROD_ENGINE_URI
    TEST_ENGINE_URI: str = model_config.TEST_ENGINE_URI
