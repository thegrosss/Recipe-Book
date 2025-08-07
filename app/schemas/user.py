from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    first_name: str
    phone_number: str
    recipes_id: list[int]

class UserLogin(BaseModel):
    id: int

# Схемы для ответа
class UserRegisterResponse(BaseModel):
    message: str
    id: int

class UserLoginResponse(BaseModel):
    message: str
    access_token: str