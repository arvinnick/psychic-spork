from typing import Any

from pydantic import BaseModel, model_validator


class SupplierBase(BaseModel):
    id: int
    name: str = ''
    address: str = None
    number: str = None
    email: str = None
    # @model_validator(mode='after')
    # @classmethod
    # def at_least_one_contact(cls, address:str, number:str, email:str) -> Any:
    #     assert (address or number or email)


class SupplierCreate(SupplierBase):
    pass




# class Supplier(Base):
#     __tablename__ = 'supplier'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     address: Mapped[str | None] = mapped_column(Text)
#     number: Mapped[str] = mapped_column(String(15))
#     email: Mapped[str | None] = mapped_column(Text)
#     inventories:Mapped[List["Inventory"]] = relationship(secondary=SupplierInventoryAssociation)

