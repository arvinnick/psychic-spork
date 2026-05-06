from sqlalchemy import Float, ForeignKey, DateTime, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from ..db.database import engine


class Base(DeclarativeBase):
    pass


SupplierInventoryAssociation = Table(
    "supplier_inventory_association",
    Base.metadata,
    Column("supplier_id", ForeignKey("supplier.id"), primary_key=True),
    Column("inventory_id", ForeignKey("inventory.id"), primary_key=True)
)



if __name__ == "__main__":
    Base.metadata.create_all(engine)