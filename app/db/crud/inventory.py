from typing import List

from sqlalchemy import update, insert
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from fastapi import HTTPException

from app.core.logger import logger
from app.db.retrievers import retrieve_inventory
from app.db.models import Inventory, Base
from app.db.deleters import entity_deleter
from app.db.models import SupplierInventoryAssociation


async def get_ingredients_db_level(db:AsyncSession,
                                   ingredient_id: List[int]|int|None= None,
                                   ingredient_name: str|List[str]|None=None,
                                   first_item = False,
                                   quantity_to:float|None= None,
                                   quantity_from:float|None= None,
                                   supplier_id: List[int]|int|None= None,
                                   slug:bool=False) -> Inventory|List[Inventory]:
    logger.info("getting ingredients db level")
    try:
        ingredient_objs = await retrieve_inventory(db=db,
                                                   ingredient_id=ingredient_id,
                                                   ingredient_name=ingredient_name,
                                                   quantity_to=quantity_to,
                                                   quantity_from=quantity_from,
                                                   supplier_id=supplier_id,
                                                   slug=slug)
        if first_item:
            return ingredient_objs.first()
        else:
            return ingredient_objs.all()
    except Exception as e:
        logger.error("An error occurred while retrieving ingredients: " + str(e))
        raise HTTPException(status_code=500, detail="An error occurred and we don't know what it is")


async def db_layer_delete_inventory(db:AsyncSession,
                                    ingredient_id:int|List[int]) -> Base|List[Base]:
    logger.info(f"deleting inventory items at db layer: {ingredient_id}")
    try:
        objs = await entity_deleter(db=db, model=Inventory, id=ingredient_id)
    except HTTPException as he:
        if he.status_code == 409:
            raise he
    except Exception as e:
        logger.error(f"an error in db layer for inventory deletion: {e}")
        raise HTTPException(500, detail="we got an error, we don't know what it is:(")
    return objs


async def db_layer_update_inventory(db:AsyncSession,
                                    engine:AsyncEngine,
                                    ingredient_id:int,
                                    form_data:dict,
                                    first_item:bool=True) -> Inventory:
    logger.info(f"updating inventory items at db layer: {ingredient_id}")
    try:
        query = update(Inventory).where(Inventory.id == ingredient_id).values(**form_data).returning(Inventory)
        updated_ingredient = await db.execute(query)
    except Exception as e:
        logger.error(f"an error in db layer for inventory update: {e}")
        raise e
    try:
        await db.commit()
        if first_item:
            return_value = updated_ingredient.scalars().first()
        else:
            return_value = updated_ingredient.scalars().all()
    except Exception as e:
        logger.error(f"an error in db layer for inventory update: {e}")
        raise e
    return return_value


async def database_layer_add_supplier_to_ingredient(engine:AsyncEngine,
                                                    ingredient_id:int,
                                                    values_to_be_added):
    logger.info(f"adding supplier to ingredient: {ingredient_id} at the database layer")
    values = []
    for (ingred_id, supp_id) in values_to_be_added:
        values.append({
            "inventory_id":ingred_id
            ,"supplier_id":supp_id})
    query = insert(SupplierInventoryAssociation).values(values)
    try:
        async with engine.begin() as conn:
            return_value = await conn.execute(query)
    except Exception as e:
        logger.error(e)
        raise e
    return return_value
