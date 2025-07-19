from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str

class UserAdd(BaseModel):
    first_name: str = Field(min_length=3, max_length=20, description="Имя пользователя")
    last_name: str = Field(min_length=3, max_length=20, description="Фамилия пользователя")
    phone_number: str = Field(description="Номер телефона, начиная с '+'")