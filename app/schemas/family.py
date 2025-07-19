from pydantic import BaseModel
from app.schemas.user import User

class FamilyCreate(BaseModel):
    pass

class Family(BaseModel):
    id: int
    members: list(User)