from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str]
    phone_number: Mapped[str]

    recipes: Mapped[list["Recipe"]] = relationship(
        back_populates="owners",
        secondary="users_recipes",
        lazy="selectin"
    )

class UserRecipes(Base):
    __tablename__ = "users_recipes"

    user_id = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True
    )