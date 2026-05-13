from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import Inventory, Supplier
from app.db.database import get_db
from schemas.inventory import InventoryCreate
from schemas.inventory import Inventory as SchemasInventory

inventory_crud_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)

@inventory_crud_router.post("/", response_model=SchemasInventory, status_code=201)
async def create_inventory_item(inventory_item: InventoryCreate,
        db: Annotated[Session, Depends(get_db)],
                                ):
    try:
        supplier_names = inventory_item.suppliers
        suppliers = db.execute(select(Supplier).where(Supplier.name.in_(supplier_names))).scalars().all()
        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier names are not in the database. You need to add them"
                                                        "first or use the correct id.")
        db_item = Inventory(
            name=inventory_item.name,
            quantity=inventory_item.quantity,
            suppliers=suppliers
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            return HTTPException(status_code=500, detail=str(e))
