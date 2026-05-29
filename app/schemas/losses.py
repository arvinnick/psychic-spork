from pydantic.types import datetime
from pydantic import BaseModel, Field

from app.schemas.inventory import Inventory


class Loss(BaseModel):
    date_time: datetime = Field(default_factory=lambda:datetime.now())
    ingredient : Inventory
    quantity : float = Field(gt=0, description="The quantity of the inventory item. Must be a positive float number.")


class LossesCreate(Loss):
    ingredient: str

class LossesRead(Loss):
    ingredient: str
    quantity: float
    date_time: str

