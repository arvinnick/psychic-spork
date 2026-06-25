from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy import event

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


@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # the sqlite3 driver will not set PRAGMA foreign_keys
    # if autocommit=False; set to True temporarily
    ac = dbapi_connection.autocommit
    dbapi_connection.autocommit = True

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

    # restore previous autocommit setting
    dbapi_connection.autocommit = ac



# Alternative: Session with transaction control
async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """
    Provides a session that automatically begins a transaction.
    Useful when you need explicit transaction boundaries.
    """
    async with async_session_maker() as session:
        async with session.begin():
            yield session