from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.schemas.user import User, UserRegisterResponse, UserLoginResponse, UserLogin
from app.repository.user import Repository

from app.auth.auth import auth, config
from app.core.config import user_tokens

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: Annotated[User, Depends()]):
    user = await Repository.find_user(phone_number=user_data.phone_number)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь уже зарегистрирован")

    user_id = await Repository.create_user(user_data)

    return UserRegisterResponse(
        message=f"Пользователь {user_data.first_name} успешно зарегистрирован",
        id=user_id
    )

@router.post("/login", response_model=UserLoginResponse)
async def login(user_data: Annotated[UserLogin, Depends()], response: Response):
    user = await Repository.find_user(id=user_data.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Такого пользователя не существует")

    token = auth.create_access_token(uid=str(user_data.id), subject=user_data.id)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

    user_tokens[user_data.id] = token

    return UserLoginResponse(
        message=f"Добро пожаловать, {user.first_name}!",
        access_token=token
    )