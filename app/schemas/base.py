from pydantic import BaseModel



class SupplierInventoryAssociation(BaseModel):
    id: int
    supplier: int
    inventory: int