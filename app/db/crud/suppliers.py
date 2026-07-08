
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from typing_extensions import List

from app.db.models import Supplier, Base
from app.core.logger import logger
from app.db.retrievers import retrieve_suppliers_by_id
from app.db.deleters import entity_deleter


async def db_layer_retrieve_supplier(db:AsyncSession,
                                     supplier_id:int|List[int]|None=None,
                                     first_item=False) -> List[Supplier]:
    logger.info("Getting order by the specified constraints")
    suppliers = await retrieve_suppliers_by_id(
        db=db, supplier_id=supplier_id, first_item=first_item
    )
    return suppliers


async def db_layer_delete_supplier(db:AsyncSession,
                                    supplier_id:int|List[int]) -> Base|List[Base]:
    logger.info(f"deleting supplier items at db layer: {supplier_id}")
    try:
        objs = await entity_deleter(db=db, model=Supplier, id=supplier_id)
    except HTTPException as he:
        if he.status_code == 409:
            raise he
    except Exception as e:
        logger.error(f"an error in db layer for inventory deletion: {e}")
        raise HTTPException(500, detail="we got an error, we don't know what it is:(")
    return objs


async def db_layer_update_supplier(db:AsyncSession,
                                    supplier_id:int,
                                    form_data:dict,
                                    first_item:bool=True) -> Supplier:
    logger.info(f"updating supplier items at db layer: {supplier_id}")
    try:
        query = update(Supplier).where(Supplier.id == supplier_id).values(**form_data).returning(Supplier)
        updated_supplier = await db.execute(query)
    except Exception as e:
        logger.error(f"an error in db layer for inventory update: {e}")
        raise e
    try:
        await db.commit()
        if first_item:
            return_value = updated_supplier.scalars().first()
        else:
            return_value = updated_supplier.scalars().all()
    except Exception as e:
        logger.error(f"an error in db layer for supplier update: {e}")
        raise e
    return return_value
