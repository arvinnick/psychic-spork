from typing import List
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import Inventory
from app.core.logger import logger
from app.db.crud.inventory import get_ingredients_db_level
from db.retrievers import retrieve_inventory


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



