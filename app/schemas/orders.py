from datetime import datetime as datetime_factory
from pydantic import BaseModel, Field
from pydantic.types import datetime
from app.schemas.inventory import Inventory
from app.schemas.supplier import SupplierBase


class Order(BaseModel):
    date_time: datetime = Field(default_factory=lambda:datetime_factory.now())
    quantity: float| int = Field(gt=0,
                                 description="The quantity of the order. Must be a positive float number.")
    ingredient: Inventory
    supplier: SupplierBase

class OrderCreate(Order):
    ingredient: str
    supplier: str

