from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query

import app.core.config as config
from app.db.database import get_db
from app.db.models import Supplier
from app.core.logger import logger
from app.schemas.supplier import SupplierCreate
from app.schemas.supplier import SupplierBase as SupplierSchema
from app.schemas.supplier import Supplier as SupplierList
from app.schemas.inventory import InventoryGet as InventoryList
from app.db.injectors import db_item_injector
from app.services.supplier import get_suppliers, service_delete_supplier
from app.db.models import Inventory
from app.services.inventory import get_ingredients
from app.routers.crud.commons import delete_item

suppliers_crud_router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)
logger.info("Defined the suppliers router.")


@suppliers_crud_router.post('/',
                            response_model=SupplierSchema,
                            summary="Create a new supplier entity in the DB",
                            status_code=201)
async def create_supplier(supplier: SupplierCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Endpoint to create a new supplier entity in the database. The supplier is the business which will fullfill
    an order.
    """
    logger.info(f"Creating a new supplier with name: {supplier.name}")
    try:
        db_item = Supplier(
            **supplier.model_dump()
        )
        await db_item_injector(db_item, db)
        return db_item
    except Exception as e:
        logger.error(f"error in creating suppliers endpoint: {e}")
        raise HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")


@suppliers_crud_router.get('',
                           response_model=SupplierList,
                           summary="getter endpoint for selected database entites",
                           status_code=200)
async def get_suppliers_endpoint(db: Annotated[AsyncSession, Depends(get_db)],
                                 supplier_id:Annotated[int|List[int]|None, Query()]=None) -> List[Supplier]:
    logger.info("Getting all suppliers in router level")
    try:
        supplier_objs = await get_suppliers(db,
                                            supplier_id)
        return supplier_objs
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")


@suppliers_crud_router.get('/{supplier_id}',
                           response_model=SupplierList,
                           summary="getter endpoint for all database entites",
                           status_code=200)
async def get_supplier_item_endpoint(db: Annotated[AsyncSession, Depends(get_db)],
                                 supplier_id: int) -> List[Supplier]:
    logger.info("Getting all suppliers in router level")
    try:
        supplier_objs = await get_suppliers(db, supplier_id)
        return supplier_objs
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")


@suppliers_crud_router.get('/{supplier_id}/ingredients',
                           response_model=InventoryList,
                           summary="getter endpoint for all database entities",
                           status_code=200)
async def get_suppliers_ingredient_endpoint(db: Annotated[AsyncSession, Depends(get_db)],
                                 supplier_id: int) -> List[Inventory]:
    logger.info("Getting all suppliers in router level")
    try:
        supplier_objs = await get_ingredients(db=db, supplier_id=supplier_id)
        return supplier_objs
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")


###delete operations
@suppliers_crud_router.delete("/{supplier_id}",
                              status_code=204,
                              summary="deleting a supplier")
async def delete_supplier_item(db: Annotated[AsyncSession, Depends(get_db)],
                                supplier_id: int):
    logger.info(f"deleting inventory object: {supplier_id}")
    #check if it exists
    try:
        deleted_item = await delete_item(db=db, item_id=supplier_id,
                                             getter_func=get_suppliers, model=Supplier,
                                             service_delete_function=service_delete_supplier)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in deleting inventory object: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we know no more")
    return deleted_item


@suppliers_crud_router.delete("",
                              status_code=204,
                              summary="deleting an inventory item (ingredient)")
async def delete_inventory_list(db: Annotated[AsyncSession, Depends(get_db)],
                                supplier_id: Annotated[List[int]|int, Query()]):
    logger.info(f"deleting supplier object(s): {supplier_id}")
    try:
        deleted_item = await delete_item(db=db, item_id=supplier_id,
                                             getter_func=get_suppliers, model=Supplier,
                                             service_delete_function=service_delete_supplier)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in deleting inventory object: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we know no more")
    return deleted_item