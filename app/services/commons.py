from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base as BaseDBModel
from app.core.logger import logger


async def check_if_item_exists(db:AsyncSession,
                                  item_id: int|None,
                                  model:BaseDBModel,
                                  getter_func:callable) -> bool:
    # check if it exists
    try:
        objects = await getter_func(db,
                                    item_id)

        if not objects:
            return False
        else:
            return True

    except Exception as e:
        if isinstance(e, HTTPException):
            if e.status_code == 404:
                raise e
            else:
                pass
        logger.error(
            f"error in deleting {model.name} object, checking for existence: {e}"
        )
        raise HTTPException(
            500, "something went wrong and we don't know what it is:("
        )