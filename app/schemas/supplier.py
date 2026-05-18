from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, model_validator, EmailStr
from typing_extensions import Self

class SupplierBase(BaseModel):
    name: str = ''
    address: str = None
    number: str = None
    email: EmailStr | None = None


class SupplierCreate(SupplierBase):
    @model_validator(mode='after')
    def at_least_one_contact(self) -> Self:
        if not (self.address or self.number or self.email):
            raise RequestValidationError('you should add at least one of the ways to contact the supplier')
        return self




