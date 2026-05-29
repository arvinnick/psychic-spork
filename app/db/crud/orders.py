from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import app.config as config
from app.db.database import get_db
from app.db.models import Inventory, Supplier
from app.logger import logger
from app.schemas.orders import Order as SchemasOrder
from app.schemas.orders import OrderCreate
from app.db.models import Orders

orders_crud_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
logger.info("Defined the orders router.")


@orders_crud_router.post("/",
                         response_model=SchemasOrder,
                         summary="creates an order entity in the database",
                         status_code=201)
async def create_order(order: OrderCreate, db:Annotated[AsyncSession, Depends(get_db)]) -> Orders | None:
    """
    Path operation for creating an order entity in the database. Orders are somehow "messages" that will be sent to a
    supplier to send an ingredient to the kitchen.
    """
    logger.info("Creating order for ingredient: {order.ingredient} from supplier: {order.supplier}.")
    try:
        smth = select(Inventory).where(Inventory.name == order.ingredient)
        ingredients = await db.execute(
            smth
        )
        ingredients = ingredients.scalars()
        ingredient = ingredients.first()
        if not ingredient:
            raise HTTPException(status_code=400, detail="Ingredient not found in the database.")
        supliers_db_object = await db.execute(select(Supplier).where(Supplier.name == order.supplier))
        suppliers = supliers_db_object.scalars().all()
        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier not found in the database.")
        ingred_suppliers = await ingredient.awaitable_attrs.suppliers
        ingredient_suppliers_ids = [supp.id for supp in ingred_suppliers]
        req_suppliers_ids = [sup.id for sup in suppliers]
        if not set(ingredient_suppliers_ids).intersection(set(req_suppliers_ids)):
            raise HTTPException(status_code = 400,
                                detail = "non of the mentioned suppliers provide the requested ingredient.")
        order_supplier = suppliers[0]
        db_item = Orders(
            date_time=order.date_time,
            quantity = order.quantity,
            ingredient = ingredient,
            supplier = order_supplier
        )
        db.add(db_item)
        await db.commit()
        return db_item
    except Exception as e:
        if isinstance(e, HTTPException):
            if e.status_code == 400:
                raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")