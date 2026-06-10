from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.config as config
from app.db.database import get_db
from app.core.logger import logger
from app.schemas.orders import Order as SchemasOrder, OrderGet
from app.schemas.orders import OrderCreate
from app.db.models import Orders
from app.db.crud.orders import db_layer_create_order, db_layer_retrieve_order

orders_crud_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
logger.info("Defined the orders router.")


@orders_crud_router.post("/",
                         response_model=SchemasOrder,
                         summary="creates an order entity in the database",
                         status_code=201)
async def create_order(order: OrderCreate, db:Annotated[AsyncSession, Depends(get_db)]) -> List[Orders] | None:
    """
    Path operation for creating an order entity in the database. Orders are somehow "messages" that will be sent to a
    supplier to send an ingredient to the kitchen.
    """
    logger.info(f"Creating order for ingredient: {order.ingredient} from supplier: {order.supplier}.")
    try:
        db_item = await db_layer_create_order(db, order)
        return db_item
    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code in [400,404]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")


@orders_crud_router.get("/{order_id}",
                        response_model=OrderGet,
                        summary="order retrieval",
                        status_code=200
                        )
async def get_order_by_id(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:int=None,
                    ingredient_id:int=None,
                    supplier_id:int=None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None,
                    ) -> Orders:
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
        return db_item[0] #todo: this is not the best way I can imagine.
    except Exception as e:
        if isinstance(e, HTTPException) and e.status_code in [400,404]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
