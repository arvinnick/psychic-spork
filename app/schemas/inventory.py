from pydantic import BaseModel, Field, RootModel
from typing import List

from app.schemas.supplier import SupplierBase


class InventoryBase(BaseModel):
    name: str
    quantity: float = Field(ge=0, description="The quantity of the inventory item. Must be a positive float number.")

class Inventory(InventoryBase):
    suppliers: List[SupplierBase]


class InventoryCreate(Inventory):
    suppliers: List[str]

class InventoryGet(RootModel[List[InventoryBase]]):
    pass


class InventoryPutItem(InventoryBase):
    pass

class InventoryPutResponse(InventoryBase):
    pass