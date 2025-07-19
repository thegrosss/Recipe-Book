from pydantic import BaseModel
from app.schemas.user import User

class FamilyCreate(BaseModel):
    name: str

class FamilyCreateResponse(BaseModel):
    message: str
    family_id: int

class FamilyUserAddResponse(BaseModel):
    message: str
    id: int

class FamilyUser(BaseModel):
    id: int
    first_name: str
    last_name: str