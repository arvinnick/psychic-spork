from pydantic import BaseModel, model_validator, EmailStr
from typing_extensions import Self
from pydantic_extra_types.phone_numbers import PhoneNumber


class SupplierBase(BaseModel):
    name: str = ''
    address: str | None = None
    number: PhoneNumber | None = None
    email: EmailStr | None = None


class SupplierCreate(SupplierBase):
    @model_validator(mode='after')
    def at_least_one_contact(self) -> Self:
        if not (self.address or self.number or self.email):
            raise ValueError('you should add at least one of the ways to contact the supplier.')
        return self




