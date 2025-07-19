from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]

    # Отношения с другими таблицами
    recipes = relationship("Recipe", back_populates="owner")
    family = relationship("FamilyUser", back_populates="user")