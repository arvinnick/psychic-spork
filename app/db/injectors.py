from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.db.models import Base
from core.logger import logger
from db.models import SupplierInventoryAssociation


async def db_item_injector(db_item:Base, db:AsyncSession):
    """
    Injects a database item into the database.
    :param db_item: an instance of a database model
    :param db: dependency of a
    """
    db.add(db_item)
    await db.flush()


async def database_layer_add_ingredient_to_supplier(
    engine: AsyncEngine, supplier_id: int, values_to_be_added
):
    logger.info(
        f"adding ingredient to supplier: {supplier_id} at the database layer"
    )
    values = []
    for ingred_id, supp_id in values_to_be_added:
        values.append({"inventory_id": ingred_id, "supplier_id": supp_id})
    query = insert(SupplierInventoryAssociation).values(values)
    try:
        async with engine.begin() as conn:
            return_value = await conn.execute(query)
    except Exception as e:
        logger.error(e)
        raise e
    return return_value
