from typing import Awaitable, Callable, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base as BaseDBModel
from app.core.logger import logger
from services.commons import check_if_item_exists


async def delete_item(db: AsyncSession,
                      item_id: List[int]|int,
                      model:BaseDBModel,
                      getter_func:Callable,
                      service_delete_function:Callable,
                      ):
    logger.info(f"deleting {model.__tablename__} object: {item_id}")
    #check if it exists
    try:
        existence_of_obj = await check_if_item_exists(db, item_id, model, getter_func)
    except Exception as e:
        logger.error(f"error in deleting inventory object: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we know no more")
    if not existence_of_obj:
        logger.info(f"no inventory item found for inventory id: {item_id}")
        raise HTTPException(status_code=404, detail="ID doesn't exist")
    try:
        deleted_inventory = await service_delete_function(db, item_id)
        if deleted_inventory:
            return []
        else:
            raise Exception(f"there was a problem in deleting {item_id}")
    except HTTPException as he:
        if he.status_code == 409:
            logger.error(he)
            raise he
    except Exception as e:
        logger.error(f"error in deleting loss object: {e}")
        raise HTTPException(500,"something went wrong and we don't know what it is:(")
