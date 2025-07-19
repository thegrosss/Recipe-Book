from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class ShoppingList(Base):
    __tablename__ = "shopping"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int]
    items: Mapped[str]