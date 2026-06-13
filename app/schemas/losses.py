from typing import List

from pydantic.types import datetime
from pydantic import BaseModel, Field, RootModel

from app.schemas.inventory import Inventory


class LossBase(BaseModel):
    date_time: datetime = Field(default_factory=lambda:datetime.now())
    quantity : float = Field(gt=0, description="The quantity of the inventory item. Must be a positive float number.")

class Loss(LossBase):
    ingredient : Inventory

class LossesCreate(LossBase):
    ingredient: str

class LossGetItem(LossBase):
    ingredient_id: int

class LossGet(RootModel[List[LossGetItem]]):
    pass
