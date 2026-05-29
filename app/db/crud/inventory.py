from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
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
        smth = select(Supplier).where(Supplier.name.in_(supplier_names))
        suppliers_db_object = await db.execute(smth)
        suppliers = suppliers_db_object.scalars().all()
        if not suppliers:
            raise HTTPException(status_code=400, detail="Supplier names are not in the database. You need to add them "
                                                        "first or use the correct id.")
        db_item = Inventory(
            name=inventory_item.name,
            quantity=inventory_item.quantity,
            suppliers=suppliers
        )
        db.add(db_item)
        await db.commit()
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
