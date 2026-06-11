from datetime import datetime as datetime_factory
from typing import List

from pydantic import BaseModel, Field, RootModel
from pydantic.types import datetime
from app.schemas.inventory import Inventory
from app.schemas.supplier import SupplierBase


class OrderBase(BaseModel):
    date_time: datetime = Field(default_factory=lambda:datetime_factory.now())
    quantity: float| int = Field(gt=0,
                                 description="The quantity of the order. Must be a positive float number.")

class Order(OrderBase):
    ingredient: Inventory
    supplier: SupplierBase

class OrderCreate(Order):
    ingredient: str
    supplier: str

class OrderGetItem(OrderBase):
    supplier_id: int
    ingredient_id: int

class OrderGet(RootModel[List[OrderGetItem]]):
    pass

