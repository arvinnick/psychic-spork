from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.config as config
from app.db.models import Inventory
from app.db.database import get_db
from app.core.logger import logger
from app.core.config import settings
from app.schemas.inventory import InventoryCreate
from app.schemas.inventory import Inventory as SchemasInventory

from sqlalchemy.exc import IntegrityError

from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_suppliers

inventory_crud_router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)
logger.info("Defined the inventory router.")

@inventory_crud_router.post("/",
                            response_model=SchemasInventory,
                            status_code=201)
async def create_inventory_item(inventory_item: InventoryCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
                                ) -> Inventory:
    logger.info(f"Creating inventory item: {inventory_item.name}")
    try:
        supplier_names = inventory_item.suppliers
        if not supplier_names:
            raise HTTPException(status_code=400, detail="You must define at least one supplier for an ingredient")
        suppliers = await retrieve_suppliers(supplier_names, db)
        db_item = Inventory(
            name=inventory_item.name,
            quantity=inventory_item.quantity,
            suppliers=suppliers
        )
        await db_item_injector(db_item, db)
        return db_item
    except IntegrityError as ie:
        if "unique constraint" in " ".join(ie.args).lower():
            await db.rollback()
            raise HTTPException(status_code=409,
                                detail=f"An inventory item with the name {inventory_item.name} already exists."
                                )
        else:
            raise ie

    except Exception as e:
        if settings.DEBUG:
            if isinstance(e, HTTPException):
                raise e
            else:
                raise HTTPException(status_code=500,
                                    detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
