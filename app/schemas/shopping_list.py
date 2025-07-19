from pydantic import BaseModel
from app.schemas.user import User

class ShoppingList(BaseModel):
    title: str
    items: str
    owner: User

class ShoppingListAdd(BaseModel):
    title:str
    items: str