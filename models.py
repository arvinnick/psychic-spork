from sqlalchemy import String, Float, Text, ForeignKey, DateTime, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


SupplierInventoryAssociation = Table(
    "supplier_inventory_association",
    Base.metadata,
    Column("supplier_id", ForeignKey("supplier.id"), primary_key=True),
    Column("inventory_id", ForeignKey("inventory.id"), primary_key=True)
)

class Supplier(Base):
    __tablename__ = 'supplier'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str | None] = mapped_column(Text)
    inventories:Mapped[List["Inventory"]] = relationship(secondary=SupplierInventoryAssociation)



class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    quantity:Mapped[float] = mapped_column(Float)
    suppliers: Mapped[List["Supplier"]] = relationship(
        secondary=SupplierInventoryAssociation,
        back_populates="inventories"
    )



class Losses(Base):
    __tablename__ = "losses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    ingredient: Mapped[Inventory] = relationship("Inventory")
    quantity: Mapped[float] = mapped_column(Float)

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    quantity: Mapped[float] = mapped_column(Float)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    ingredient: Mapped[Inventory] = relationship("Inventory")
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id"))
    supplier: Mapped[Supplier] = relationship("Supplier")



