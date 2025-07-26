from pydantic import BaseModel

class ShoppingList(BaseModel):
    id: int
    owner_id: int
    title: str
    items: str

class ShoppingListAdd(BaseModel):
    title: str
    items: str

class ShoppingListAddResponse(BaseModel):
    message: str = "Список продуктов успешно добавлен"
    id: int