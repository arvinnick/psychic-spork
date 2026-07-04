from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from app.db.models import Losses
from app.core.logger import logger
from app.db.crud.losses import (
    db_layer_get_losses,
    db_layer_delete_losses,
    db_layer_update_loss,
)
from app.services.commons import check_if_item_exists
from app.internals.helpers import datetime_converter


async def get_losses(
    db: AsyncSession,
    loss_id: List[int] | int | None = None,
    ingredient_id: List[int] | int | None = None,
    datetime_to: str | None = None,
    datetime_from: str | None = None,
    quantity_lt: float | None = None,
    quantity_gt: float | None = None,
) -> List[Losses]:
    try:
        return await db_layer_get_losses(db, loss_id, ingredient_id, datetime_to, datetime_from, quantity_lt,
                                         quantity_gt)
        
        
    except HTTPException as he:
        logger.error(f"validation error in getting losses in service layer: {he}")
        raise he
    except Exception as e:
        logger.error(f"something happened in getting orders on the service layer: {e}")
        raise HTTPException(500, "Something went wrong and we don't know what it is:(")



async def service_delete_loss(
        db: AsyncSession,
        loss_id: List[int]|int) -> List[int]|int|None:
    logger.info(f"deleting loss: {loss_id} at the service layer")
    try:
        deleted_loss_object = await db_layer_delete_losses(db=db, loss_id=loss_id)
    except HTTPException as he:
        logger.error(f"error in deleting loss: {he}")
        raise he
    if isinstance(loss_id, int):
        if deleted_loss_object == [loss_id]:
            return loss_id
        else:
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )
    elif isinstance(loss_id, list):
        if deleted_loss_object == loss_id:
            return loss_id
        else:
            return JSONResponse(
                status_code=HTTP_204_NO_CONTENT, content={"detail": "ID doesn't exist"}
            )


# async def check_if_loss_id_exists(db: AsyncSession, loss_id: List[int]|int) -> bool:
#     # check if it exists
#     try:
#         loss_objects = await get_losses(db, loss_id)
#         if isinstance(loss_id, list):
#             if len(loss_objects) == len(loss_id):
#                 return True
#         elif isinstance(loss_id, int):
#             if loss_objects:
#                 return True
#         else:
#             raise TypeError("Loss_id is not int")
#         return False
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             if e.status_code == 404:
#                 raise e
#             else:
#                 logger.error(f"error in check_if_loss_id_exists: {e}")
#                 pass
#         else:
#             logger.error(f"error in deleting loss object, checking for existence: {e}")
#             raise HTTPException(
#                 500, "something went wrong and we don't know what it is:("
#             )


async def check_if_loss_id_exists(db:AsyncSession,
                                        loss_id: List[int]|int) -> bool:
    try:
        existence = await check_if_item_exists(db, loss_id, Losses, get_losses)
    except HTTPException as he:
        logger.error(f"error in check_if_loss_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_loss_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existence


async def service_layer_update_loss(db: AsyncSession,
                                    item_id:int,
                                    form_data: dict,
                                    engine=None,
                                    first_item:bool=True) -> Losses:
    loss_id = item_id
    logger.info(f"updating loss object: {loss_id} at the service layer")
    try:
        existence = await check_if_loss_id_exists(db=db, loss_id=loss_id)
    except HTTPException as he:
        logger.error(f"error in updating loss object: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in updating loss object: {e}")
        raise e
    if existence:
        try:
            form_data["date_time"] = datetime_converter(
                form_data.get("date_time")
            )
            updated_loss = await db_layer_update_loss(
                db=db,
                loss_id=loss_id,
                form_data=form_data,
                first_item=first_item,
            )
        except HTTPException as he:
            logger.error(f"error in updating loss object: {he}")
            raise he
        except Exception as e:
            logger.error(f"error in updating loss object: {e}")
            raise e
        return updated_loss
    else:
        return None