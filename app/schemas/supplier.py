from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator, EmailStr
from typing_extensions import Self

class SupplierBase(BaseModel):
    name: str = ''
    address: str = None
    number: str = None
    email: EmailStr = None


class SupplierCreate(SupplierBase):
    @model_validator(mode='after')
    def at_least_one_contact(self) -> Self:
        if not (self.address or self.number or self.email):
            raise RequestValidationError('you should add at least one of the ways to contact the supplier')
        return self




# class Supplier(Base):
#     __tablename__ = 'supplier'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     address: Mapped[str | None] = mapped_column(Text)
#     number: Mapped[str] = mapped_column(String(15))
#     email: Mapped[str | None] = mapped_column(Text)
#     inventories:Mapped[List["Inventory"]] = relationship(secondary=SupplierInventoryAssociation)

