from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

if settings.PROD:
    engine = create_async_engine(settings.PROD_ENGINE_URI, echo=False)
else:
    engine = create_async_engine(settings.DEV_ENGINE_URI, echo=True if settings.DEBUG else False,
                                 )





async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy loading issues after commit

)



# Alternative: Session with transaction control
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """
    Provides a session that automatically begins a transaction.
    Useful when you need explicit transaction boundaries.
    """
    async with async_session_maker() as session:
        async with session.begin():
            yield session