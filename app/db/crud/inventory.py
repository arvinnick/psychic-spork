from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

import app.config as config
from app.db.models import Inventory, Supplier
from app.db.database import get_db
from app.logger import logger
from app.config import settings
from app.schemas.inventory import InventoryCreate
from app.schemas.inventory import Inventory as SchemasInventory

from sqlalchemy.exc import IntegrityError

inventory_crud_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)
logger.info("Defined the inventory router.")

@inventory_crud_router.post("/", response_model=SchemasInventory, status_code=201)
async def create_inventory_item(inventory_item: InventoryCreate,
        db: Annotated[Session, Depends(get_db)],
                                ):
    logger.info(f"Creating inventory item: {inventory_item.name}")
    try:
        supplier_names = inventory_item.suppliers
        if not supplier_names:
            raise HTTPException(status_code=400, detail="You must define at least one supplier for an ingredient")
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
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail=f"An inventory item with {inventory_item.name} already exists."
                            )

    except Exception as e:
        if settings.DEBUG:
            if isinstance(e, HTTPException):
                raise e
            else:
                return HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
        else:
            return HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
