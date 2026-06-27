from typing import Annotated, List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.supplier import get_suppliers_for_ingredient
from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_inventory, retrieve_suppliers_by_name, retrieve_orders
from app.db.database import get_db
from app.schemas.orders import OrderCreate
from app.db.models import Orders
from app.core.logger import logger
from app.db.deleters import deleter


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
        raise HTTPException(status_code=400,
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


async def db_layer_retrieve_order(db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:List[int]=None,
                    ingredient_id:List[int]=None,
                    supplier_id:List[int]=None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None) -> List[Orders]:
    logger.info("Getting order by the specified constraints")
    orders = await retrieve_orders(
        db=db,
        order_id=order_id,
        ingredient_id=ingredient_id,
        supplier_id=supplier_id,
        date_time_from=date_time_from,
        date_time_to=date_time_to,
        quantity_lt=quantity_lt,
        quantity_gt=quantity_gt
    )
    return orders



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