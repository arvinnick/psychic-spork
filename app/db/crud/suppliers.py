from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from app.db.database import get_db
from app.db.models import Supplier, Base
from app.core.logger import logger
from app.db.retrievers import retrieve_suppliers_by_id
from app.db.deleters import deleter


async def db_layer_retrieve_supplier(db:Annotated[AsyncSession, Depends(get_db)],
                                     supplier_id:int|List[int]|None=None) -> List[Supplier]:
    logger.info("Getting order by the specified constraints")
    suppliers = await retrieve_suppliers_by_id(
        db=db, supplier_id=supplier_id
    )
    return suppliers


async def db_layer_delete_supplier(db:AsyncSession,
                                    supplier_id:int|List[int]) -> Base|List[Base]:
    logger.info(f"deleting supplier items at db layer: {supplier_id}")
    try:
        objs = await deleter(db=db,
                             model=Supplier,
                             id=supplier_id)
    except HTTPException as he:
        if he.status_code == 409:
            raise he
    except Exception as e:
        logger.error(f"an error in db layer for inventory deletion: {e}")
        raise HTTPException(500, detail="we got an error, we don't know what it is:(")
    return objs