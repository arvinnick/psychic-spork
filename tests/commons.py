import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import Base


async def seed_db(engine, model_base = Base):
    if os.path.exists(engine.url.database):
        os.remove(engine.url.database)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(model_base.metadata.create_all)
    except Exception as e:
        raise e



async def async_session_maker(engine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Prevent lazy loading issues after commit
    )


