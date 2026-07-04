from datetime import datetime
from typing import Annotated, List

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger

from app.db.database import get_db
from app.db.models import Supplier, Inventory, Losses, SupplierInventoryAssociation
from app.db.models import Orders


async def retrieve_suppliers_by_name(supplier_names:List[str],
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


async def retrieve_inventory(db:AsyncSession,
                             model=Inventory,
                             ingredient_name:str|List[str]|None=None,
                             ingredient_id: List[int]|int|None=None,
                             quantity_to:float|None=None,
                             quantity_from:float|None=None,
                             supplier_id: List[int]|int|None= None,
                             slug:bool=False):
    """
    
    """

    if supplier_id:
        if isinstance(supplier_id, list):
            query = select(model).join(
        SupplierInventoryAssociation, Inventory.id == SupplierInventoryAssociation.c.inventory_id).join(
        Supplier, SupplierInventoryAssociation.c.supplier_id == Supplier.id
    ).where(Supplier.id.in_(supplier_id))
        elif isinstance(supplier_id, int):
            query = (
                select(model)
                .join(
                    SupplierInventoryAssociation,
                    Inventory.id == SupplierInventoryAssociation.c.inventory_id,
                )
                .join(
                    Supplier, SupplierInventoryAssociation.c.supplier_id == Supplier.id
                )
                .where(Supplier.id == supplier_id))
    else:
        query = select(model)
    if ingredient_name:
        if isinstance(ingredient_name, str):
            if slug:
                query = query.where(model.name_slug == ingredient_name).options(
                    selectinload(model.suppliers))
            else:
                query = query.where(model.name == ingredient_name).options(
                    selectinload(model.suppliers)
                )
        elif isinstance(ingredient_name, list):
            if slug:
                query = query.where(model.name_slug.in_(ingredient_name)).options(
                selectinload(model.suppliers)
            )
            else:
                query = query.where(model.name.in_(ingredient_name)).options(
                    selectinload(model.suppliers)
                )
    if ingredient_id:
        if isinstance(ingredient_id, list):
            query = query.where(model.id.in_(ingredient_id)).options(
            selectinload(model.suppliers))
        elif isinstance(ingredient_id, int):
            query = query.where(model.id == ingredient_id).options(
                selectinload(model.suppliers)
            )
        else:
            raise HTTPException(status_code=422, detail="Incorrect ingredient id.")
        

    if quantity_to:
        query = query.where(model.quantity <= quantity_to)
    if quantity_from:
        query = query.where(model.quantity >= quantity_from)
    try:
        ingredients_db_object = await db.execute(query)
    except Exception as e:
        logger.error("An error occurred while retrieving inventory: " + str(e))
        raise e
    ingredients = ingredients_db_object.scalars()
    return ingredients



async def retrieve_orders(
                    db:Annotated[AsyncSession, Depends(get_db)],
                    order_id:List[int]=None,
                    ingredient_id:List[int]=None,
                    supplier_id:List[int]=None,
                    date_time_from:datetime|None=None,
                    date_time_to: datetime|None=None,
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
            query = query.where(Orders.date_time >= date_time_from)
        if date_time_to:
            query = query.where(Orders.date_time <= date_time_to)
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
    return orders



async def retrieve_losses(db:Annotated[AsyncSession, Depends(get_db)],
                          loss_id:List[int]|int|None=None,
                          ingredient_id:List[int]|int|None=None,
                          datetime_to: str | None = None,
                          datetime_from: str | None = None,
                          quantity_lt: float | None = None,
                          quantity_gt: float | None = None,
                          ):
    logger.info("retrieving losses by the specified constraints")
    query = select(Losses).options(selectinload(Losses.ingredient))
    try:
        if loss_id:
            if isinstance(loss_id, list):
                query = query.where(Losses.id.in_(loss_id))
            elif loss_id:
                query = query.where(Losses.id == loss_id)
            else:
                raise HTTPException(status_code=422, detail="Invalid loss_id parameter. It should be either a list of integers or a single integer.")
        if ingredient_id:
            if isinstance(ingredient_id, list):
                query = query.where(Losses.ingredient_id.in_(ingredient_id))
            else:
                raise HTTPException(status_code=422, detail="Invalid ingredient_id parameter. It should be a list of integers.")
        if datetime_from:
            query = query.where(Losses.date_time >= datetime.fromisoformat(datetime_from))
        if datetime_to:
            query = query.where(Losses.date_time <= datetime.fromisoformat(datetime_to))
        if quantity_lt:
            query = query.where(Losses.quantity <= quantity_lt)
        if quantity_gt:
            query = query.where(Losses.quantity >= quantity_gt)
    except ValueError as ve:
        logger.error(f"validation error in retrieving losses endpoint: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"An error occurred while retrieving losses: {str(e)}")
        raise e
    losses = await db.execute(query)
    losses = losses.scalars().all()
    return losses

async def retrieve_suppliers_by_id(
        db:Annotated[AsyncSession, Depends(get_db)],
        supplier_id:List[int]|int|None = None
                                   ) -> List[Supplier]:
    logger.info("retrieving suppliers by id")
    query = select(Supplier).options(selectinload(Supplier.inventories))
    if isinstance(supplier_id, int):
        query = query.where(Supplier.id == supplier_id)
    elif isinstance(supplier_id, list):
        query = query.where(Supplier.id.in_(supplier_id))
    try:
        suppliers = await db.execute(query)
        suppliers = suppliers.scalars().all()
    except Exception as e:
        logger.error(f"An error occurred while retrieving suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail="we have gotten an error. We know no more")
    return suppliers



async def retrieve_suppliers_for_ingredient(ingredient: str,
                                       db:AsyncSession) -> List[Supplier]:
    """
    the service function to check if the records of the supplier in the database indicates whether they provide the ingredint
    :param suppliers: list of sqlalchemy objects for supplier record
    :param ingredient: sqlalchemy object for ingredient record
    :return: boolean result showing if the supplier provides the ingredient or not
    """
    supplier_ingredient_overlap_query = select(Supplier
                                               ).join(
        SupplierInventoryAssociation, Supplier.id == SupplierInventoryAssociation.c.supplier_id).join(
        Inventory, SupplierInventoryAssociation.c.inventory_id == Inventory.id
    ).where(Inventory.name == ingredient)

    supplier_ingredient_result = await db.execute(supplier_ingredient_overlap_query)
    return supplier_ingredient_result.scalars().all()