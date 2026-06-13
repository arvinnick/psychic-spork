from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Losses
from app.core.logger import logger
from app.db.crud.losses import db_layer_get_orders


async def get_losses(
    db: AsyncSession,
    loss_id: List[int] | None = None,
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