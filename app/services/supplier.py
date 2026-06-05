from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from typing import Annotated

from app.db.database import get_db
from db.models import Supplier, Inventory, SupplierInventoryAssociation


async def retrieve_suppliers_for_ingredient(ingredient: str,
                                       db:Annotated[AsyncSession, Depends(get_db)]):
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


