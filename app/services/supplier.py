from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from typing import List

from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from app.db.models import Supplier
from app.core import config
from app.db.crud.suppliers import (
    db_layer_retrieve_supplier,
    db_layer_delete_supplier,
    db_layer_update_supplier,
)
from app.db.crud.inventory import get_ingredients_db_level
from app.db.retrievers import retrieve_suppliers_for_ingredient as db_layer_supplier_ingredient_retriever
from app.services.commons import (
    check_if_item_exists,
)
from core.logger import logger
from services.inventory import check_if_ingredient_id_exists


async def get_suppliers(
        db:AsyncSession,
        supplier_id:int|List[int]|None=None,
        first_item=False
) -> List[Supplier]:
    logger.info("Getting suppliers by the specified constraints")
    try:
        db_item = await db_layer_retrieve_supplier(db,
                                                   supplier_id,
                                                   first_item=first_item)
        return db_item
    except Exception as e:
        logger.error(f"service layer, getting suppliers, has encountered an error: {e}")
        if isinstance(e, HTTPException) and e.status_code in [400, 422]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")

async def get_suppliers_for_ingredient(db:AsyncSession,
                                       ingredient_id:int,
                                       ingredient_obj=None) -> List[Supplier]:
    logger.info("get_suppliers_for_ingredient is calleds")
    if ingredient_obj is None:
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
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )
    elif isinstance(supplier_id, list):
        if deleted_loss_object == supplier_id:
            return supplier_id
        else:
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )



async def service_layer_update_supplier(db:AsyncSession,
    item_id:int,
    form_data:dict,
    first_item:bool=True,
                                        engine:AsyncEngine=None) -> Supplier:
    supplier_id = item_id
    logger.info(f"updating supplier: {supplier_id} at the service layer")
    try:
        existence = await check_if_supplier_id_exists(db=db, supplier_id=supplier_id)
    except HTTPException as he:
        logger.error(f"error in updating supplier: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in updating supplier: {e}")
        raise e
    if existence:
        try:
            updated_supplier = await db_layer_update_supplier(db=db,
                                                             supplier_id=supplier_id,
                                                             form_data=form_data,
                                                             first_item=first_item)
        except HTTPException as he:
            logger.error(f"error in updating supplier: {he}")
            raise he
        except Exception as e:
            logger.error(f"error in updating supplier: {e}")
            raise e
        return updated_supplier
    else:
        return None





async def check_if_supplier_id_exists(db:AsyncSession,
                                        supplier_id: List[int]|int) -> bool:
    logger.info(f"checking if {supplier_id} exists as an ingredient")
    try:
        existence = await check_if_item_exists(db, supplier_id, Supplier, get_suppliers)
    except HTTPException as he:
        logger.error(f"error in check_if_supplier_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_supplier_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existence

