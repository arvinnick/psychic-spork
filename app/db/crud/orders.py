from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

import app.config as config
from app.db.database import get_db
from app.db.models import Inventory, Supplier
from app.logger import logger
from app.schemas.orders import Order as SchemasOrder, OrderCreate
from app.db.models import Orders

orders_crud_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)
logger.info(f"Defined the orders router.")


@orders_crud_router.post("/", response_model=SchemasOrder,
                         summary="creates an order entity in the database",
                         status_code=201)
def create_order(order: OrderCreate, db:Annotated[Session, Depends(get_db)]) -> Orders:
    """
    Path operation for creating an order entity in the database. Orders are somehow "messages" that will be sent to a
    supplier to send an ingredient to the kitchen.
    """
    logger.info("Creating order for ingredient: {order.ingredient} from supplier: {order.supplier}.")
    try:
        ingredients = db.execute(select(Inventory).where(Inventory.name == order.ingredient)).scalars().all()
        if not ingredients:
            raise HTTPException(status_code=400, detail="Ingredient not found in the database.")
        ingredient = ingredients[0]
        suppliers = db.execute(select(Supplier).where(Supplier.name == order.supplier)).scalars().all()
        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier not found in the database.")

        ingredient_suppliers_ids = [supp.id for supp in ingredient.suppliers]
        req_suppliers_ids = [supp.id for supp in suppliers]
        if not set(ingredient_suppliers_ids).intersection(set(req_suppliers_ids)):
            raise HTTPException(status_code = 400,
                                detail = "non of the mentioned suppliers provide the requested ingredient.")

        db_item = Orders(
            date_time=order.date_time,
            quantity = order.quantity,
            ingredient = ingredients[0],
            supplier = suppliers[0]
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        if e.__getattribute__("status_code") == 400:
            raise e
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")