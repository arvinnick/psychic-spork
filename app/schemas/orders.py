from pydantic import BaseModel, model_validator
from pydantic.types import datetime
from datetime import datetime as vanilla_datetime
from schemas.inventory import Inventory
from schemas.supplier import SupplierBase


class Order(BaseModel):
    quantity: float
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