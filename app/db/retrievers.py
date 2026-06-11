from datetime import datetime
from typing import Annotated, List

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger

from app.db.database import get_db
from app.db.models import Supplier, Inventory
from app.db.models import Orders


async def retrieve_suppliers(supplier_names:List[str],
                             db: Annotated[AsyncSession, Depends(get_db)],
                             model = Supplier):
    """
    The
    :param supplier_names:
    :param db:
    :return:
    """
    smth = select(model).where(model.name.in_(supplier_names))
    suppliers_db_object = await db.execute(smth)
    suppliers = suppliers_db_object.scalars().all()
    if not suppliers:
        raise HTTPException(status_code=404, detail="Supplier not found in the database.")
    return suppliers


async def retrieve_inventory(ingredient_name:str, db:Annotated[AsyncSession, Depends(get_db)],
                             model=Inventory):
    """
    
    :param supplier_id: 
    :return: 
    """
    smth = select(model).where(model.name == ingredient_name).options(
        selectinload(model.suppliers))
    ingredients_db_object = await db.execute(smth)
    ingredients = ingredients_db_object.scalars().first()
    if ingredients is None:
        raise HTTPException(status_code=404, detail="Ingredient not found in the database.")
    return ingredients



async def retrieve_orders(
                    db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:List[int]=None,
                    ingredient_id:List[int]=None,
                    supplier_id:List[int]=None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None
            )  -> List[Orders]:
    logger.info("retrieving orders by the specified constraints")
    query = select(Orders)
    try:
        if order_id:
            if isinstance(order_id, list):
                query = query.where(Orders.id.in_(order_id))
            else:
                query = query.where(Orders.id == order_id)
        if ingredient_id:
            query = query.where(Orders.ingredient_id.in_(ingredient_id))#.options(selectinload(Orders.ingredient))
        if supplier_id:
            query = query.where(Orders.supplier_id.in_(supplier_id))#.options(selectinload(Orders.supplier)).options(selectinload(Orders.supplier.inventories))
        if date_time_from:
            query = query.where(Orders.date_time >= datetime.fromisoformat(date_time_from))
        if date_time_to:
            query = query.where(Orders.date_time <= datetime.fromisoformat(date_time_to))
        if quantity_lt:
            query = query.where(Orders.quantity <= quantity_lt)
        if quantity_gt:
            query = query.where(Orders.quantity >= quantity_gt)

        query = query.options(
        selectinload(Orders.ingredient).selectinload(Inventory.suppliers),
        selectinload(Orders.supplier).selectinload(Supplier.inventories),
    )
        orders_cor = await db.execute(query)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred while retrieving orders: {str(e)}")
        raise e
    orders = orders_cor.scalars().all()
    if not any([
        ingredient_id,
        supplier_id,
        date_time_from,
        date_time_to,
        quantity_lt,
        quantity_gt
    ]):
        if not orders:
            raise HTTPException(status_code=404, detail="No orders with specified id(s).")
    return orders