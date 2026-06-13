from typing import List, Annotated

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.orders import db_layer_retrieve_order
from app.db.models import Orders
from app.core.logger import logger
from app.core import config
from app.db.database import get_db


async def get_orders(db:Annotated[AsyncSession, Depends(get_db)],
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



