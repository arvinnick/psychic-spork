import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.models import Base
from app.db import database
from app.core.logger import logger


async def main(engine: AsyncEngine = database.engine, model_base = Base):
    try:
        logger.info("initiating the database seeding process...")
        async with engine.begin() as conn:
            await conn.run_sync(model_base.metadata.create_all)
        logger.info("database seeded successfully")
    except Exception as e:
        raise e

if __name__ == "__main__":
    asyncio.run(main())