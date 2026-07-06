from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.supplier import get_suppliers_for_ingredient, get_suppliers
from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_inventory, retrieve_suppliers_by_name
from app.schemas.orders import OrderCreate
from app.db.models import Orders
from app.core.logger import logger
from app.db.deleters import deleter
from db.crud.commons import db_layer_updater
from app.services.commons import check_if_item_exists
from db.crud.inventory import get_ingredients_db_level
from db.models import Supplier
from schemas.inventory import Inventory
from services.commons import get_orders


async def db_layer_order_id_checker(db:AsyncSession,
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

async def db_layer_create_order(db:AsyncSession, order: OrderCreate) -> Orders:
    # this function is the database layer for creating an order. it is separated from the path operation function to make it testable without the need for the whole app and its dependencies
    supplier = order.supplier
    ingredient = order.ingredient

    ingredient_obj = await retrieve_inventory(db,
                                              ingredient_name=ingredient)
    ingredient_obj = ingredient_obj.first()
    try:
        sup_of_ingred = await get_suppliers_for_ingredient(db=db, ingredient_id=ingredient_obj.id)
    except AttributeError as ae:
        logger.error(f"something has happened in db.crud.orders: {ae}")
        if ingredient_obj is None:
            raise HTTPException(status_code=400,
                                detail="no such ingredient in the database.")
    except Exception as e:
        logger.error("An error occurred while retrieving suppliers for ingredient: " + str(e))
        raise e
    if supplier not in [supp.name for supp in sup_of_ingred]:
        try:
            await retrieve_suppliers_by_name([supplier], db)
        except HTTPException as e:
            raise e
        raise HTTPException(status_code=409,
                            detail="non of the mentioned suppliers provide the requested ingredient.")
    supplier_objs = await retrieve_suppliers_by_name([supplier], db)
    supplier_obj = supplier_objs[0]#todo: there should be a mechanism for the user to choose the supplier if there are multiple suppliers providing the ingredient. for now we just choose the first one
    db_item = Orders(
        date_time=order.date_time,
        quantity=order.quantity,
        ingredient=ingredient_obj,
        supplier=supplier_obj
    )
    await db_item_injector(db_item, db)
    return db_item



async def db_layer_delete_order(
    order_id:List[int]|int,
        db:AsyncSession,

):
    logger.info(f"deleting order items at db layer: {order_id}")
    try:
        objs = await deleter(db=db, model=Orders, id=order_id)
    except HTTPException as he:
        if he.status_code == 409:
            raise he
    except Exception as e:
        logger.error(f"an error in db layer for order deletion: {e}")
        raise HTTPException(500, detail="we got an error, we don't know what it is:(")
    return objs


async def db_layer_update_order(
        db:AsyncSession,
        loss_id:int,
        form_data:dict,
        first_item:bool,
        existence_cache:object
):
    '''

    '''
    logger.info(f"updating order items at db layer: {loss_id}")
    logger.info(f"checking if ingredient id {form_data.get("ingredient_id")} exists")
    try:
        ingredient_exists = await check_if_item_exists(db, form_data.get("ingredient_id"), Inventory, get_ingredients_db_level)
        if not ingredient_exists:
            raise HTTPException(status_code=204,detail="ingredient doesn't exist")
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    logger.info(f"checking supplier id {form_data.get("supplier_id")} existence")
    try:
        supplier_exists = await check_if_item_exists(db, form_data.get("supplier_id"), Supplier,
                                               get_suppliers)
        if not supplier_exists:
            raise HTTPException(status_code=204,detail="supplier doesn't exist")
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    try:
        updated_obj = await db_layer_updater(
            db=db,
            item_id=loss_id,
            form_data=form_data,
            first_item=first_item,
            model=Orders,
            db_layer_id_checker=db_layer_order_id_checker,
            existence_cache=existence_cache
        )
    except IntegrityError as ie:
        logger.error(f"integrity error in db_layer_update_order: {ie}")
        if "FOREIGN KEY" in str(ie):
            raise HTTPException(detail="supplier doesn't provide the ingredient",
                                status_code=409)
    except Exception as e:
        logger.error(f"an error in db layer updater: {e}")
        raise e
    return updated_obj