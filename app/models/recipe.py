from sqlalchemy import ForeignKey

from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    instruction: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)