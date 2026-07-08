import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from app.db.models import Base
from app.db import database
from app.core.logger import logger


async def main(engine: AsyncEngine = database.engine, model_base = Base):
    try:
        logger.info("initiating the database seeding process...")
        async with engine.begin() as conn:
            await conn.run_sync(model_base.metadata.create_all)
            await conn.execute(text("PRAGMA foreign_keys=ON;"))
        logger.info("database seeded successfully")
    except Exception as e:
        logger.error(f"seeding db error: {e}")
        raise e

if __name__ == "__main__":
    asyncio.run(main())