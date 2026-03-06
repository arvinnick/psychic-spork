from pydantic import BaseModel


class Inventory(BaseModel):
    code:str
    name:str
    quantity:float

