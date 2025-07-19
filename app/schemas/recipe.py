from pydantic import BaseModel
from app.schemas.user import User

class Recipe(BaseModel):
    id: int
    title: str
    description: str
    instructions: str
    owner: User

class RecipeAdd(BaseModel):
    title: str
    description: str
    instructions: str