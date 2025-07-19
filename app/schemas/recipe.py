from pydantic import BaseModel
from app.schemas.user import User

class Recipe(BaseModel):
    id: int
    title: str
    description: str
    instruction: str
    owner_id: int

class RecipeAdd(BaseModel):
    title: str
    description: str
    instruction: str

class RecipeOut(BaseModel):
    id: int
    title: str
    description: str
    instruction: str

class RecipeAddResponse(BaseModel):
    message: str = "Рецепт успешно добавлен"
    id: int