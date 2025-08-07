from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger

class ShoppingList(Base):
    __tablename__ = "shopping"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id = mapped_column(BigInteger)
    title: Mapped[str]
    items: Mapped[str]