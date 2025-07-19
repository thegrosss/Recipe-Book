from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    members = relationship("FamilyUser", back_populates="family")

class FamilyUser(Base):
    __tablename__ = "family_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user = relationship("User", back_populates="family")
