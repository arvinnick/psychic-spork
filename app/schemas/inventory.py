from pydantic import BaseModel
from typing import List

from app.schemas.supplier import SupplierBase


class Inventory(BaseModel):
    name: str
    quantity: int = 0
    suppliers: List[SupplierBase]

class InventoryCreate(Inventory):
    suppliers: List[str]