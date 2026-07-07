from sqlalchemy import (
    ForeignKey,
    Column,
    Table,
    DateTime,
    String,
    Float,
    Text,
    func,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from datetime import datetime
from typing import List



class Base(AsyncAttrs, DeclarativeBase):
    pass

class SluggMaker:
    @hybrid_property
    def name_slug(self) -> str:
        """Python-side: converts 'Olive Oil' → 'olive-oil'"""
        return self.name.lower().replace(" ", "-")

    @name_slug.expression
    def name_slug(cls):
        """SQL-side: applies the same transformation in the database"""
        return func.replace(func.lower(cls.name), " ", "-")

SupplierInventoryAssociation = Table(
    "supplier_inventory_association",
    Base.metadata,
    Column("supplier_id",
           ForeignKey("supplier.id",
                      ondelete="SET NULL",
                      onupdate="CASCADE")),
    Column("inventory_id",
           ForeignKey("inventory.id",
                      ondelete="SET NULL",
                      onupdate="CASCADE")),
    PrimaryKeyConstraint(
        "supplier_id",
        "inventory_id"
    )
)

class Inventory(Base, SluggMaker):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50), unique=True)
    quantity:Mapped[float] = mapped_column(Float)
    suppliers: Mapped[List["Supplier"]] = relationship(
        secondary=SupplierInventoryAssociation,
        back_populates="inventories"
    )


class Supplier(Base, SluggMaker):
    __tablename__ = 'supplier'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str | None] = mapped_column(Text)
    inventories:Mapped[List["Inventory"]] = relationship(secondary=SupplierInventoryAssociation,
                                                         back_populates="suppliers")

class Losses(Base):
    __tablename__ = "losses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id",
                                                          ondelete="RESTRICT",
                                                          onupdate="CASCADE"),
                                               nullable=False)
    ingredient: Mapped[Inventory] = relationship()
    quantity: Mapped[float] = mapped_column(Float)

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    quantity: Mapped[float] = mapped_column(Float)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id", ondelete="RESTRICT"))
    ingredient: Mapped[Inventory] = relationship("Inventory")
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id", ondelete="RESTRICT"))
    supplier: Mapped[Supplier] = relationship("Supplier")
    
    # __table_args__ = (ForeignKeyConstraint([ingredient_id, supplier_id],
    #                                        [
    #                                            SupplierInventoryAssociation.c.inventory_id,
    #                                            SupplierInventoryAssociation.c.supplier_id
    #                                        ]),)
