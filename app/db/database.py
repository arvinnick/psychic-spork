from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config import settings
from app.logger import logger

if settings.PROD:
    engine = create_async_engine(settings.PROD_ENGINE_URI, echo=True)
else:
    engine = create_async_engine(settings.TEST_ENGINE_URI, echo=True)

async def get_db():
    db = AsyncSession(engine)
    logger.info("Getting db session")
    try:
        yield db
    finally:
        await db.close()
