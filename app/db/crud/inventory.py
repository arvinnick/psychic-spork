from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.core.logger import logger
from app.db.retrievers import retrieve_inventory
from db.models import Inventory


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
