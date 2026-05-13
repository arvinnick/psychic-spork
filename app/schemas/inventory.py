from pydantic import BaseModel, model_validator
from typing import List

from app.schemas.supplier import SupplierBase


class Inventory(BaseModel):
    name: str
    quantity: float = 0
    suppliers: List[SupplierBase]
    @model_validator(mode='after')
    def validate_quantity(self):
        assert self.quantity >= 0, "Inventory quantity must be positive float number"
        return self

class InventoryCreate(Inventory):
    suppliers: List[str]