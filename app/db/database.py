from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import settings
from logger import logger

if settings.PROD:
    engine = create_engine(settings.PROD_ENGINE_URI, echo=True)
else:
    engine = create_engine(settings.TEST_ENGINE_URI, echo=True)

async def get_db():
    db = Session(engine)
    logger.info(f"Getting db session")
    try:
        yield db
    finally:
        db.close()
