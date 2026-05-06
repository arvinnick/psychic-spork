from pydantic import BaseModel

from .base import SupplierInventoryAssociation


class Inventory(BaseModel):
    id: int
    name: str
    quantity: float
    supplier: SupplierInventoryAssociation