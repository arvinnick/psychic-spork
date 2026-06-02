from app.db.models import Supplier, Inventory
from typing import Collection


async def supplier_provides_ingredient(suppliers: Collection[Supplier], ingredient: Inventory) -> bool:
    """
    the service function to check if the records of the supplier in the database indicates whether they provide the ingredint
    :param suppliers: list of sqlalchemy objects for supplier record
    :param ingredient: sqlalchemy object for ingredient record
    :return: boolean result showing if the supplier provides the ingredient or not
    """
    ingred_suppliers = await ingredient.awaitable_attrs.suppliers
    ingredient_suppliers_ids = [supp.id for supp in ingred_suppliers]
    req_suppliers_ids = [sup.id for sup in suppliers]
    if not set(ingredient_suppliers_ids).intersection(set(req_suppliers_ids)):
        return False
    return True
