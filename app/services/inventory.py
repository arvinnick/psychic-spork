from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from app.db.models import Inventory
from app.core.logger import logger
from app.db.crud.inventory import (
    get_ingredients_db_level,
    db_layer_delete_inventory,
    db_layer_update_inventory,
    db_layer_update_ingred_supp_relation,
)
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
    logger.info(f"checking if {ingredient_id} exists as an ingredient")
    try:
        existence = await check_if_item_exists(db, ingredient_id, Inventory, get_ingredients)
    except HTTPException as he:
        logger.error(f"error in check_if_ingredient_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_ingredient_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existence



async def service_delete_ingredient(db:AsyncSession,
                                    ingredient_id:List[int]|int|None)-> List[int]|int|None:
    logger.info(f"deleting inventory item: {ingredient_id} at the service layer")
    try:
        deleted_loss_object = await db_layer_delete_inventory(db=db, ingredient_id=ingredient_id)
    except HTTPException as he:
        logger.error(f"error in deleting inventory: {he}")
        raise he
    if isinstance(ingredient_id, int):
        if deleted_loss_object == [ingredient_id]:
            return ingredient_id
        else:
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )
    elif isinstance(ingredient_id, list):
        if deleted_loss_object == ingredient_id:
            return ingredient_id
        else:
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )


async def service_layer_update_ingredient(db:AsyncSession,
                                          engine:AsyncEngine,
                                          item_id:int,
                                          form_data:dict,
                                          first_item:bool=True) -> List[Inventory]:
    ingredient_id = item_id
    logger.info(f"updating ingredient: {ingredient_id} at the service layer")
    try:
        existence = await check_if_ingredient_id_exists(db=db, ingredient_id=ingredient_id)
    except HTTPException as he:
        logger.error(f"error in updating ingredient: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in updating ingredient: {e}")
        raise e
    if existence:
        try:
            supplier_ids = form_data.pop("suppliers")
            await update_supply_ingred_association(engine=engine, ingredient_id=ingredient_id,
                                                                               supplier_ids=supplier_ids)
        except Exception as e:
            logger.error(f"error in assigning suppliers ingredient: {e}")
            raise e
        try:
            updated_ingredient = await db_layer_update_inventory(db=db,
                                                                 engine=engine,
                                                                 ingredient_id=ingredient_id,
                                                                 form_data=form_data,
                                                                 supplier_ids=supplier_ids,
                                                                 first_item=first_item)
        except HTTPException as he:
            logger.error(f"error in updating ingredient: {he}")
            raise he
        except Exception as e:
            logger.error(f"error in updating ingredient: {e}")
            raise e
        return updated_ingredient
    else:
        return None


async def update_supply_ingred_association(engine:AsyncEngine,ingredient_id:int,
                               supplier_ids:List[int]):
    logger.info(f"updating ingredient: {ingredient_id} at the service layer")
    try:
        await db_layer_update_ingred_supp_relation(
            engine=engine,
            ingredient_id=ingredient_id,
            supplier_ids=supplier_ids
        )
    except Exception as e:
        logger.error(f"error in updating ingredient supplier relation: {e}")
        raise e
