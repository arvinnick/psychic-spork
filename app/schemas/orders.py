from pydantic import BaseModel, model_validator, Field
from pydantic.types import datetime
from datetime import datetime as vanilla_datetime
from schemas.inventory import Inventory
from schemas.supplier import SupplierBase


class Order(BaseModel):
    date_time: datetime = Field(default_factory=datetime.now)
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