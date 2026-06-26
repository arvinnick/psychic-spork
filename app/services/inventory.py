from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Inventory
from app.core.logger import logger
from app.db.crud.inventory import get_ingredients_db_level, db_layer_delete_inventory
from app.services.commons import check_if_item_exists


async def get_ingredients(db:AsyncSession,
                          ingredient_id: List[int]|int|None = None,
                          ingredient_name: str|List[str]|None=None,
                          first_item:bool=False,
                          quantity_to:float|None=None,
                          quantity_from:float|None=None,
                          supplier_id:int|List[int]|None=None,
                          slug:bool=False) -> List[Inventory]|Inventory:
    logger.info("getting ingredients at service level")
    try:
        inventory_objects = await get_ingredients_db_level(db,
                                                           ingredient_id=ingredient_id,
                                                           ingredient_name=ingredient_name,
                                                           first_item=first_item,
                                                           quantity_to=quantity_to,
                                                           quantity_from=quantity_from,
                                                           supplier_id=supplier_id,
                                                           slug=slug)
        return inventory_objects
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500,
                            detail="we have gotten an error and we don't know what it is")



async def check_if_ingredient_id_exists(db:AsyncSession,
                                        ingredient_id: int|None) -> bool:
    try:
        existance = await check_if_item_exists(db, ingredient_id, Inventory, get_ingredients)
    except HTTPException as he:
        logger.error(f"error in check_if_ingredient_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_ingredient_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existance



async def service_delete_ingredient(db:AsyncSession,
                                    ingredient_id:List[int]|int|None)-> List[int]|int|None:
    logger.info(f"deleting inventory item: {ingredient_id} at the service layer")
    try:
        deleted_loss_object = await db_layer_delete_inventory(db=db, ingredient_id=ingredient_id)
    except HTTPException as he:
        logger.error(f"error in deleting loss: {he}")
        raise he
    if isinstance(ingredient_id, int):
        if deleted_loss_object == [ingredient_id]:
            return ingredient_id
        else:
            raise HTTPException
    elif isinstance(ingredient_id, list):
        if deleted_loss_object == ingredient_id:
            return ingredient_id
        else:
            raise HTTPException