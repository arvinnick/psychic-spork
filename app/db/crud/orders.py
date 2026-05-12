from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Inventory, Supplier
from schemas.orders import Order as SchemasOrder, OrderCreate
from app.db.models import Orders
from sqlalchemy import select



orders_crud_router = APIRouter(
    prefix="/orders",
)

@orders_crud_router.post("/", response_model=SchemasOrder)
def create_order(order: OrderCreate, db:Annotated[Session, Depends(get_db)]) -> Orders:
    try:
        ingredients = db.execute(select(Inventory).where(Inventory.name == order.ingredient)).scalars().all()
        if not ingredients:
            raise HTTPException(status_code=400, detail="Ingredient not found in the database")
        elif len(ingredients) > 1:
            raise HTTPException(status_code=400, detail=f"There are {len(ingredients)} ingredients in the database with this name")
        suppliers = db.execute(select(Supplier).where(Supplier.name == order.supplier)).scalars().all()
        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier not found in the database")
        elif len(suppliers) > 1:
            raise HTTPException(status_code=400, detail=f"There are {len(suppliers)} suppliers in the database with this name")
        db_item = Orders(
            date_time=datetime.now(),
            quantity = order.quantity,
            ingredient = ingredients[0],
            supplier = suppliers[0]
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

