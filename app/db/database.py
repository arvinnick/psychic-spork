from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import settings

if settings.PROD:
    engine = create_engine(settings.PROD_ENGINE_URI, echo=True)
else:
    engine = create_engine(settings.TEST_ENGINE_URI, echo=True)

async def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
