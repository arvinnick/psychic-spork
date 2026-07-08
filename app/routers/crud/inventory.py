from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.db.models import Inventory
from app.db.database import get_db, get_engine
from app.core.logger import logger
from app.core.config import settings
from app.schemas.inventory import (
    InventoryCreate,
    InventoryGet,
    InventoryPutResponse,
)
from app.schemas.inventory import Inventory as SchemasInventory
from app.schemas.supplier import Supplier as SupplierListSchema

from sqlalchemy.exc import IntegrityError

from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_suppliers_by_name
from app.services.inventory import (
    get_ingredients,
    service_delete_ingredient,
    service_layer_update_ingredient,
)
from app.db.models import Supplier
from app.services.supplier import get_suppliers_for_ingredient
from app.routers.crud.commons import delete_item
from app.schemas.inventory import InventoryPutItem
from app.routers.crud.commons import update_item
from app.services.supplier_inventory_relationship import service_layer_add_supplier_to_ingredient

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
        if he.status_code in [409, 400, 204]:
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
                        ingredient_id:Annotated[int|List[int], Query()]=None,
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
                                               ingredient_id=ingredient_id,
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



###delete operations
@inventory_crud_router.delete("/{ingredient_id}",
                              status_code=204,
                              summary="deleting an inventory item (ingredient)")
async def delete_inventory_item(db: Annotated[AsyncSession, Depends(get_db)],
                                ingredient_id: int):
    logger.info(f"deleting inventory object: {ingredient_id}")
    #check if it exists
    try:
        deleted_item = await delete_item(db=db, item_id=ingredient_id,
                                             getter_func=get_ingredients, model=Inventory,
                                             service_delete_function=service_delete_ingredient)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in deleting inventory object: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we know no more")
    return deleted_item


@inventory_crud_router.delete("",
                              status_code=204,
                              summary="deleting an inventory item (ingredient)")
async def delete_inventory_list(db: Annotated[AsyncSession, Depends(get_db)],
                                ingredient_id: Annotated[List[int]|int, Query()]):
    logger.info(f"deleting inventory object(s): {ingredient_id}")
    try:
        deleted_item = await delete_item(db=db, item_id=ingredient_id,
                                             getter_func=get_ingredients, model=Inventory,
                                             service_delete_function=service_delete_ingredient)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in deleting inventory object: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we know no more")
    return deleted_item



#put (update)
@inventory_crud_router.put("/{ingredient_id}",status_code=200,
                           response_model=InventoryPutResponse)
async def update_inventory_item(
        db: Annotated[AsyncSession, Depends(get_db)],
        engine: Annotated[AsyncEngine, Depends(get_engine)],
        ingredient_id:int,
        ingredient: InventoryPutItem,
) -> List[Inventory]:
    logger.info(f"updating inventory object: {ingredient_id}")
    form_data = jsonable_encoder(ingredient)
    try:
        returned_obj = await update_item(service_layer_update_ingredient,
                                   item_id=ingredient_id,
                                   engine=engine,
                                   db=db,
                                   form_data=form_data)
    except Exception as e:
        raise e
    return returned_obj



###supplier ingredient relationship


@inventory_crud_router.post("/{ingredient_id}/suppliers/{supplier_id}",
                           status_code=200,
                           summary="adding a supplier to the ingredient")
async def add_supplier_to_inredient(engine:Annotated[AsyncEngine, Depends(get_engine)],
                                    db: Annotated[AsyncSession, Depends(get_db)],
                                    ingredient_id:int,
                                    supplier_id:int):
    logger.info(f"adding supplier id {supplier_id} to the ingredient id {ingredient_id}")
    try:
        updated_combination = await service_layer_add_supplier_to_ingredient(db=db,
                                                                             engine=engine,
                                                                             ingredient_id=ingredient_id,
                                                                             supplier_id=supplier_id)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in adding supplier id: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in server and we know no more")
    return updated_combination


@inventory_crud_router.post("/{ingredient_id}",
                           status_code=200,
                           summary="adding a supplier to the ingredient")
async def add_suppliers_to_inredient(engine:Annotated[AsyncEngine, Depends(get_engine)],
                                    db: Annotated[AsyncSession, Depends(get_db)],
                                    ingredient_id:int,
                                    supplier_id:Annotated[List[int]|int, Query()]):
    logger.info(f"adding supplier id {supplier_id} to the ingredient id {ingredient_id}")
    try:
        updated_combination = await service_layer_add_supplier_to_ingredient(db=db,
                                                                             engine=engine,
                                                                             ingredient_id=ingredient_id,
                                                                             supplier_id=supplier_id)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in adding supplier ids: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in server and we know no more")
    return updated_combination