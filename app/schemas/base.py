from pydantic import BaseModel



class SupplierInventoryAssociation(BaseModel):
    id: int
    suppliers: int
    inventory: int