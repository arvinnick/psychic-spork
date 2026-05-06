from sqlalchemy import create_engine
from config import Settings

config = Settings()
PROD = config.PROD

if PROD:
    engine = create_engine(config.PROD_ENGINE_URI, echo=True)
else:
    engine = create_engine(config.TEST_ENGINE_URI, echo=True)