from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.logger import logger
from app.db.models import Losses
from app.db.retrievers import retrieve_losses
from app.db.deleters import entity_deleter
from app.db.crud.commons import db_layer_updater
from app.services.inventory import check_if_ingredient_id_exists


async def db_layer_get_losses(
    db: AsyncSession,
    loss_id: List[int] |int | None = None,
    ingredient_name: List[int] | int | None = None,
    datetime_to: str | None = None,
    datetime_from: str | None = None,
    quantity_lt: float | None = None,
    quantity_gt: float | None = None,
    first_item:bool=False
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
            first_item=first_item
        )
    except HTTPException as he:
        logger.error(f"validation error in getting losses from database: {he}")
        raise he
    except Exception as e:
        logger.error(f"database layer retrieve_losses error {e}")
        raise HTTPException(status_code=500, detail="we got an error, we don't know what it is:(")
    return losses



async def db_layer_delete_losses(db: AsyncSession, loss_id: int|List[int]) -> List[int]|int:
    logger.info(f"deleting loss at db layer: {loss_id}")
    try:
        objs = await entity_deleter(db=db, model=Losses, id=loss_id)
    except Exception as e:
        logger.error(f"an error in db layer for deletion: {e}")
        raise HTTPException(500, detail="we got an error, we don't know what it is:(")
    return objs

async def db_layer_update_loss(
        db:AsyncSession,
        loss_id: int,
        form_data:dict,
        first_item:bool=True,
existence_cach=None):
    logger.info(f"updating inventory items at db layer: {loss_id}")
    try:
        updated_obj = await db_layer_updater(
            model=Losses,
            item_id=loss_id,
            form_data=form_data,
            first_item=first_item,
            db=db,
            db_layer_id_checker=check_if_ingredient_id_exists,
            existence_cache=existence_cach
        )
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    return updated_obj