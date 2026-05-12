from pydantic.types import datetime
from pydantic import BaseModel, model_validator

from schemas.inventory import Inventory


class Loss(BaseModel):
    date_time: datetime
    ingredient : Inventory
    quantity : float
    @model_validator(mode='after')
    def no_zero_quantity(self):
        assert self.quantity > 0, 'Quantity must be positive'
        return self


class LossesCreate(Loss):
    ingredient: str
