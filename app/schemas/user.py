from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str

# Схемы для авторизации
class UserRegister(BaseModel):
    first_name: str = Field(min_length=3, max_length=20, description="Имя пользователя")
    last_name: str = Field(min_length=3, max_length=20, description="Фамилия пользователя")
    phone_number: str = Field(description="Номер телефона, начиная с '+'")
    password: str = Field(min_length=5, max_length=20, description="Пароль")

class UserLogin(BaseModel):
    phone_number: str
    password: str

# Схемы для ответа
class UserRegisterResponse(BaseModel):
    message: str
    id: int

class UserLoginResponse(BaseModel):
    message: str
    access_token: str