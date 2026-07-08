from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.orders import (
    db_layer_delete_order,
    db_layer_update_order,
)
from app.db.models import Orders
from app.core.logger import logger
from app.services.commons import check_if_item_exists, update_service_layer
from app.services.commons import get_orders
from db.crud.inventory import get_ingredients_db_level
from db.models import Inventory, Supplier
from services.losses import get_losses
from services.supplier import get_suppliers_for_ingredient, get_suppliers


async def check_if_order_id_exists(db:AsyncSession,
                                        item_id: int|None) -> bool:
    logger.info("checking if order id exists")
    order_id = item_id
    try:
        existence = await check_if_item_exists(db, order_id, Orders, get_orders)
    except HTTPException as he:
        logger.error(f"error in check_if_order_id_exists: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in check_if_order_id_exists: {e}")
        raise HTTPException(status_code=500,detail="there is an error in the server and we don't know what it is")
    return existence



async def delete_orders_service_layer(db:AsyncSession,
                        order_id:List[int]|int) -> Orders|List[Orders]:
    logger.info(f"deleting order(s): {order_id}")
    try:
        deleted_loss_object = await db_layer_delete_order(db=db, order_id=order_id)
    except HTTPException as he:
        logger.error(f"error in deleting order: {he}")
        raise he
    if isinstance(order_id, int):
        if deleted_loss_object == [order_id]:
            return order_id
        else:
            raise HTTPException(404, "ID doesn't exist")
    elif isinstance(order_id, list):
        if deleted_loss_object == order_id:
            return order_id
        else:
            raise HTTPException(404, "ID doesn't exist")


async def service_layer_update_order(
        db:AsyncSession,
        item_id:int,
        form_data:dict,
        first_item:bool=True,
        engine=None
):
    logger.info(f"updating order: {item_id} at the service layer")
    logger.info(f"checking if ingredient id {form_data.get('ingredient_id')} exists")
    try:
        ingredient_cache, ingredient_exists = await check_if_item_exists(
            db, form_data.get("ingredient_id"), Inventory, get_ingredients_db_level, first_item=first_item
        )
        if not ingredient_exists:
            raise HTTPException(status_code=204, detail="ingredient doesn't exist")
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    logger.info(f"checking supplier id {form_data.get('supplier_id')} existence")
    try:
        supplier_cache, supplier_exists = await check_if_item_exists(
            db, form_data.get("supplier_id"), Supplier, get_suppliers, first_item=first_item
        )
        if not supplier_exists:
            raise HTTPException(status_code=204, detail="supplier doesn't exist")
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    # logger.info("checking if supplier exists")
    # if not await check_if_item_exists(db=db, item_id=form_data.get('supplier_id'),
    #                                   model=Supplier, getter_func=g):
    logger.info("checking if ingredient is provided by the supplier")
    suppliers = await get_suppliers_for_ingredient(db=db,
                                                   ingredient_id=form_data.get("ingredient_id"),
                                                   ingredient_obj=ingredient_cache)
    supplier_ids = [supplier.id for supplier in suppliers]
    if form_data.get("supplier_id") not in supplier_ids:
        raise HTTPException(409, detail="supplier doesn't provide the ingredient")
    updated_order = await update_service_layer(
        item_id=item_id,
        db=db,
        form_data=form_data,
        db_layer_callable=db_layer_update_order,
        existence_checker=check_if_order_id_exists,
        first_item=first_item)
    return updated_order


async def service_layer_get_loss_ingredient(db:AsyncSession, loss_id:int):
    loss_objects = await get_losses(db, loss_id)
    return loss_objects.ingredient
