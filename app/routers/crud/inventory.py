from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Inventory
from app.db.database import get_db
from app.core.logger import logger
from app.core.config import settings
from app.schemas.inventory import InventoryCreate, InventoryGet
from app.schemas.inventory import Inventory as SchemasInventory
from app.schemas.supplier import Supplier as SupplierListSchema

from sqlalchemy.exc import IntegrityError

from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_suppliers_by_name
from app.services.inventory import get_ingredients
from app.db.models import Supplier
from services.supplier import get_suppliers_for_ingredient

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
                                ) -> Inventory | None:
    logger.info(f"Creating inventory item: {inventory_item.name}")
    try:
        supplier_names = inventory_item.suppliers
        if not supplier_names:
            raise HTTPException(status_code=400, detail="You must define at least one supplier for an ingredient")
        suppliers = await retrieve_suppliers_by_name(supplier_names, db)
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
    except HTTPException as he:
        logger.error(he.detail)
        if he.status_code in [409, 400, 404]:
            raise he
        else:
            if settings.DEBUG:
                raise HTTPException(status_code=500, detail=str(he))
            else:
                raise HTTPException(
                    status_code=500,
                    detail="we got an error on the server. we know no more:(",
                )
    except Exception as e:
        if settings.DEBUG:
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=500,
                                detail="we got an error on the server. we know no more:(")




@inventory_crud_router.get("",
                           response_model=InventoryGet,
                           status_code=200)
async def get_inventory(db: Annotated[AsyncSession, Depends(get_db)],
                        quantity_to: float|None=None,
                        quantity_from:float|None=None,
                        name:Annotated[str|List[str], Query()]=None,
                        supplier_id:Annotated[int|List[int]|None, Query()]=None) -> List[Inventory]:
    logger.info("getting inventory items")
    try:
        inventory_objs = await get_ingredients(db,
                                               quantity_to=quantity_to,
                                               quantity_from=quantity_from,
                                               ingredient_name=name,
                                               supplier_id=supplier_id,
                                               slug=True if name else False)
        return inventory_objs
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")


@inventory_crud_router.get("/{ingredient_id}",
                           response_model=InventoryGet,
                           status_code=200)
async def get_inventory_item(db: Annotated[AsyncSession, Depends(get_db)],
                             ingredient_id: int,
                             ) -> List[Inventory] | None:
    logger.info("getting inventory items")
    try:
        inventory_objs = await get_ingredients(db,
                                               ingredient_id,
                                               first_item=True)
        if inventory_objs:
            if isinstance(inventory_objs, list):
                return inventory_objs
            elif isinstance(inventory_objs, Inventory):
                return [inventory_objs]
        else:
            return []
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")


@inventory_crud_router.get("/{ingredient_id}/suppliers",
                           response_model=SupplierListSchema,
                           status_code=200)
async def get_inventory_item_suppliers(db: Annotated[AsyncSession, Depends(get_db)],
                             ingredient_id: int,
                             ) -> List[Supplier] | None:
    logger.info("getting inventory items")
    try:

        suppliers_objs = await get_suppliers_for_ingredient(db=db,
                                                            ingredient_id=ingredient_id)

        if isinstance(suppliers_objs, list):
            return suppliers_objs
        elif isinstance(suppliers_objs, Inventory):
            return [suppliers_objs]
        else:
            logger.error(f"the router's return value should be either a list or an inventory item. "
                         f"But it is {type(suppliers_objs)}")
            raise HTTPException(500, "there is a problem in server and we don't know what it is.")
    except Exception as e:
        logger.error(f"we got an error in router level: {e}")
        raise HTTPException(500, "we got an error")