from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ShoppingList(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    items: Mapped[str]

    user = relationship("User")