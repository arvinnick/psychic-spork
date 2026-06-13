from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.models import Losses
from app.db.retrievers import retrieve_losses


async def db_layer_get_orders(
    db: AsyncSession,
    loss_id: List[int] | None = None,
    ingredient_name: List[int] | int | None = None,
    datetime_to: str | None = None,
    datetime_from: str | None = None,
    quantity_lt: float | None = None,
    quantity_gt: float | None = None,
) -> List[Losses]:
    try:
        losses = await retrieve_losses(
            db,
            loss_id,
            ingredient_name,
            datetime_to,
            datetime_from,
            quantity_lt,
            quantity_gt,
        )
    except HTTPException as he:
        logger.error(f"validation error in getting losses from database: {he}")
        raise he
    except Exception as e:
        logger.error(f"database layer retrieve_losses error {e}")
        raise HTTPException(status_code=500, detail="we got an error, we don't know what it is:(")
    return losses