from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Inventory
from database import get_db
from schemas.inventory import InventoryCreate, InventoryBase

inventory_crud_router = APIRouter(
    prefix="/inventory"
)

@inventory_crud_router.post("/", response_model=InventoryBase)
async def create_inventory_item(inventory_item: InventoryCreate,
        db: Annotated[Session, Depends(get_db)],
                                ):
    try:
        db_item = Inventory(**inventory_item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(inventory_item)
        return db_item
    except Exception as e:
        raise e
