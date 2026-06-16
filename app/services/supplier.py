from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from typing import Annotated, List

from app.db.database import get_db
from app.db.models import Supplier
from app.core.logger import logger
from app.core import config
from app.db.crud.suppliers import db_layer_retrieve_supplier
from app.db.crud.inventory import get_ingredients_db_level
from app.db.retrievers import retrieve_suppliers_for_ingredient as db_layer_supplier_ingredient_retriever







async def get_suppliers(
        db:Annotated[AsyncSession, Depends(get_db)],
        supplier_id:int = None
) -> List[Supplier]:
    logger.info("Getting supppliers by the specified constraints")
    try:
        db_item = await db_layer_retrieve_supplier(db,
                                                   supplier_id)
        return db_item
    except Exception as e:
        logger.error(f"service layer, getting suppliers, has encountered an error: {e}")
        if isinstance(e, HTTPException) and e.status_code in [400,404, 422]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")

async def get_suppliers_for_ingredient(db:AsyncSession,
                                            ingredient_id:int) -> List[Supplier]:
    ingredient_obj = await get_ingredients_db_level(db, ingredient_id=ingredient_id, first_item=True)
    ingredient_name = ingredient_obj.name
    suppliers = await db_layer_supplier_ingredient_retriever(db=db, ingredient=ingredient_name)
    return suppliers
