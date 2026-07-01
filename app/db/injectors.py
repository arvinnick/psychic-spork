from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base


async def db_item_injector(db_item:Base, db:AsyncSession):
    """
    Injects a database item into the database.
    :param db_item: an instance of a database model
    :param db: dependency of a
    """
    db.add(db_item)
    await db.flush()