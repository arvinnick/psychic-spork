from pydantic import BaseModel, da
from .inventory import Inventory



class Losses(Base):
    __tablename__ = "losses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    ingredient: Mapped[Inventory] = relationship("Inventory")
    quantity: Mapped[float] = mapped_column(Float)