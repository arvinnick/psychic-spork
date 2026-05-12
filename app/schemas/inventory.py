from pydantic import BaseModel
from typing import List


class Inventory(BaseModel):
    name: str
    quantity: int = 0
    suppliers: List[str]

class InventoryCreate(Inventory):
    pass