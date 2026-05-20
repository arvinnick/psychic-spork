from pydantic import BaseModel, model_validator, Field

from app.schemas.inventory import Inventory
from app.schemas.supplier import SupplierBase


class Order(BaseModel):
    quantity: float| int
    ingredient: Inventory
    supplier: SupplierBase

class OrderCreate(Order):
    quantity: float
    ingredient: str
    supplier: str
    @model_validator(mode='after')
    def check_quantity(self):
        assert self.quantity > 0, "Quantity must be positive"
        return self

