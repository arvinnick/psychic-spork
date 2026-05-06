from typing import List
from sqlalchemy import String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from.supplier import Supplier

from .base import Base, SupplierInventoryAssociation


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    quantity:Mapped[float] = mapped_column(Float)
    suppliers: Mapped[List["Supplier"]] = relationship(
        secondary=SupplierInventoryAssociation,
        back_populates="inventories"
    )