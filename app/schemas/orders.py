from sqlalchemy import Float, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base
from .inventory import Inventory
from .supplier import Supplier


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    quantity: Mapped[float] = mapped_column(Float)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    ingredient: Mapped[Inventory] = relationship("Inventory")
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id"))
    supplier: Mapped[Supplier] = relationship("Supplier")