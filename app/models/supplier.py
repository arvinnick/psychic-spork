from typing import List
from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base


class Supplier(Base):
    __tablename__ = 'supplier'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str | None] = mapped_column(Text)
    inventories:Mapped[List["Inventory"]] = relationship(secondary=SupplierInventoryAssociation)
