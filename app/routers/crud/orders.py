from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.config as config
from app.db.database import get_db
from app.core.logger import logger
from app.schemas.orders import Order as SchemasOrder, OrderGet
from app.schemas.orders import OrderCreate
from app.schemas.supplier import SupplierBase as SchemasSupplier
from app.schemas.inventory import Inventory as SchemasIngredient
from app.db.models import Orders, Supplier, Inventory
from app.db.crud.orders import db_layer_create_order
from app.services.orders import get_orders

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
        logger.error(f"exception is risen in the order post router: {e}")
        if isinstance(e, HTTPException) and e.status_code in [400,404]:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")



@orders_crud_router.get("",
                        response_model=OrderGet,
                        summary="order retrieval",
                        status_code=200
                        )
async def get_order_by_uery_params(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:Annotated[List[int] | None, Query()] = None,
                    ingredient_id:Annotated[List[int] | None, Query()] = None,
                    supplier_id:Annotated[List[int] |None, Query()] = None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None,
                    ) -> List[Orders]:
    orders = await get_orders(db,
                     order_id,
                     ingredient_id,
                     supplier_id,
                     date_time_from,
                     date_time_to,
                     quantity_lt,
                     quantity_gt
                     )
    return orders



@orders_crud_router.get("/{order_id}",
                        response_model=OrderGet,
                        summary="order retrieval",
                        status_code=200
                        )
async def get_order_by_id_as_path_param(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:int
                    ) -> List[Orders]:
    return await get_orders(db,
                     order_id)

@orders_crud_router.get("/{order_id}/suppliers",
                        response_model=SchemasSupplier,
                        summary="order retrieval",
                        status_code=200
                        )
async def get_order_supplier(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:int
                    ) -> Supplier:
    order =  await get_orders(db,
                     order_id)
    return order[0].supplier

@orders_crud_router.get("/{order_id}/ingredients",
                        response_model=SchemasIngredient,
                        summary="order retrieval",
                        status_code=200
                        )
async def get_order_ingredient(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:int
                    ) -> Inventory:
    order =  await get_orders(db,
                     order_id)
    return order[0].ingredient