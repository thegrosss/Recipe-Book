from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.repository.user import Repository
from app.schemas.recipe import RecipeOut, Recipe
from app.schemas.user import UserAdd, UserAddResponse

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.post("")
async def create_user(user_data: Annotated[UserAdd, Depends()]):
    user = await Repository.find_user(phone_number=user_data.phone_number)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь уже существует")

    user_id = await Repository.create_user(user_data)
    return UserAddResponse(id=user_id)

@router.get("/recipes/{user_id}", response_model=list[RecipeOut])
async def get_user_recipes(user_id: int) :
    user = await Repository.find_user(id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким ID не найден")

    recipes = await Repository.get_user_recipes(user_id)

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="У этого пользователя нет рецептов")

    return recipes