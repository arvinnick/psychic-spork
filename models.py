from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass



class Supplier(Base):
    __tablename__ = 'supplier'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str | None] = mapped_column(Text)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    inventory:Mapped["Inventory"] = relationship()


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    quantity:Mapped[float] = mapped_column(Float)


