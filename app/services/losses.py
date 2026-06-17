from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Losses
from app.core.logger import logger
from app.db.crud.losses import db_layer_get_orders, db_layer_delete_losses


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
        return await db_layer_get_orders(
            db,
            loss_id,
            ingredient_id,
            datetime_to,
            datetime_from,
            quantity_lt,
            quantity_gt,
        )
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
            raise HTTPException
    elif isinstance(loss_id, list):
        if deleted_loss_object == loss_id:
            return loss_id
        else:
            raise HTTPException


async def check_if_id_exists(db: AsyncSession, loss_id: int) -> bool:
    # check if it exists
    try:
        loss_objects = await get_losses(db, loss_id)
        if not loss_objects:
            return False
        else:
            return True
    except Exception as e:
        if isinstance(e, HTTPException):
            if e.status_code == 404:
                raise e
            else:
                pass
        else:
            logger.error(f"error in deleting loss object, checking for existence: {e}")
            raise HTTPException(
                500, "something went wrong and we don't know what it is:("
            )