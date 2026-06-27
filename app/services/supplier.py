from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.db.models import Supplier
from app.core.logger import logger
from app.core import config
from app.db.crud.suppliers import db_layer_retrieve_supplier, db_layer_delete_supplier
from app.db.crud.inventory import get_ingredients_db_level
from app.db.retrievers import retrieve_suppliers_for_ingredient as db_layer_supplier_ingredient_retriever







async def get_suppliers(
        db:AsyncSession,
        supplier_id:int|List[int]|None=None
) -> List[Supplier]:
    logger.info("Getting suppliers by the specified constraints")
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




async def service_delete_supplier(db:AsyncSession,
                                    supplier_id:List[int]|int|None)-> List[int]|int|None:
    logger.info(f"deleting inventory item: {supplier_id} at the service layer")
    try:
        deleted_loss_object = await db_layer_delete_supplier(db=db, supplier_id=supplier_id)
    except HTTPException as he:
        logger.error(f"error in deleting inventory: {he}")
        raise he
    if isinstance(supplier_id, int):
        if deleted_loss_object == [supplier_id]:
            return supplier_id
        else:
            raise HTTPException(404, "ID doesn't exist")
    elif isinstance(supplier_id, list):
        if deleted_loss_object == supplier_id:
            return supplier_id
        else:
            raise HTTPException(404, "ID doesn't exist")