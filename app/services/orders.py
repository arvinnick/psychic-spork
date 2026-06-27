from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.orders import db_layer_retrieve_order, db_layer_delete_order
from app.db.models import Orders
from app.core.logger import logger
from app.core import config
from services.commons import check_if_item_exists


async def get_orders(db:AsyncSession,
                    order_id:List[int]|None = None,
                    ingredient_id:List[int]|None = None,
                    supplier_id:List[int]|None = None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None,) -> List[Orders]:

    logger.info("Getting order by the specified constraints")
    try:
        db_item = await db_layer_retrieve_order(db,
                                                order_id,
                                                ingredient_id,
                                                supplier_id,
                                                date_time_from,
                                                date_time_to,
                                                quantity_lt,
                                                quantity_gt
                                                )
        return db_item
    except Exception as e:
        logger.error(f"service layer, getting orders, has encountered an error: {e}")
        if isinstance(e, HTTPException) and e.status_code in [400,404, 422]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")


async def check_if_order_id_exists(db:AsyncSession,
                                        ingredient_id: int|None) -> bool:
    try:
        existance = await check_if_item_exists(db, ingredient_id, Orders, get_orders)
    except HTTPException as he:
        logger.error(f"error in check_if_order_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_order_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existance



async def delete_orders_service_layer(db:AsyncSession,
                        order_id:List[int]|int) -> Orders|List[Orders]:
    logger.info(f"deleting order(s): {order_id}")
    try:
        deleted_loss_object = await db_layer_delete_order(db=db, order_id=order_id)
    except HTTPException as he:
        logger.error(f"error in deleting order: {he}")
        raise he
    if isinstance(order_id, int):
        if deleted_loss_object == [order_id]:
            return order_id
        else:
            raise HTTPException(404, "ID doesn't exist")
    elif isinstance(order_id, list):
        if deleted_loss_object == order_id:
            return order_id
        else:
            raise HTTPException(404, "ID doesn't exist")

