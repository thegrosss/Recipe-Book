from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tag: Mapped[str]
    content: Mapped[str]
    image: Mapped[str] = mapped_column(nullable=True)

    owners: Mapped[list["User"]] = relationship(
        back_populates="recipes",
        secondary="users_recipes",
        lazy="selectin"
    )