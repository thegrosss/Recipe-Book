from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]

class FamilyUser(Base):
    __tablename__ = "family_users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    family_id: Mapped[int] = mapped_column(primary_key=True)
