from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    instruction = Mapped[str]

    owner = relationship("User", back_populates="recipes")