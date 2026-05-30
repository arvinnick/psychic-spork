from pydantic import BaseModel, Field
from typing import List

from app.schemas.supplier import SupplierBase


class Inventory(BaseModel):
    name: str
    quantity: float = Field(ge=0, description="The quantity of the inventory item. Must be a positive float number.")
    suppliers: List[SupplierBase]


class InventoryCreate(Inventory):
    suppliers: List[str]