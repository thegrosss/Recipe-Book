from pydantic import BaseModel

class Recipe(BaseModel):
    id: int
    tag: str
    content: str
    image: str | None = None

class RecipeAdd(BaseModel):
    image: str | None = None
    tag: str
    content: str

class RecipeOut(BaseModel):
    id: int
    image: str | None = None
    content: str

class RecipeAddResponse(BaseModel):
    message: str = "Рецепт успешно добавлен"
    id: int