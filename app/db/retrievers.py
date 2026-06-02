from typing import Annotated, List

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import Supplier, Inventory


async def retrieve_suppliers(supplier_names:List[str],
                             db: Annotated[AsyncSession, Depends(get_db)]):
    """
    The
    :param supplier_names:
    :param db:
    :return:
    """
    smth = select(Supplier).where(Supplier.name.in_(supplier_names))
    suppliers_db_object = await db.execute(smth)
    suppliers = suppliers_db_object.scalars().all()
    if not suppliers:
        raise HTTPException(status_code=400, detail="Supplier names are not in the database. You need to add them "
                                                    "first or use the correct id.")
    return suppliers


async def retrieve_inventory(ingredient_name:str, db:Annotated[AsyncSession, Depends(get_db)]):
    """
    
    :param supplier_id: 
    :return: 
    """
    smth = select(Inventory).where(Inventory.name == ingredient_name).options(
        selectinload(Inventory.suppliers))
    ingredients_db_object = await db.execute(smth)
    ingredients = ingredients_db_object.scalars().first()
    return ingredients