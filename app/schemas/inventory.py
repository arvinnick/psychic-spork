from pydantic import BaseModel

from .supplier import SupplierBase


class Inventory(BaseModel):
    name: str
    quantity: int = 0
    supplier: SupplierBase

class InventoryCreate(Inventory):
    pass