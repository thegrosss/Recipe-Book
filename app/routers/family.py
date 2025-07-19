from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.repository.family import Repository
from app.schemas.family import FamilyCreate, FamilyCreateResponse, FamilyUserAddResponse, FamilyUser
from app.schemas.recipe import Recipe

router = APIRouter(prefix="/families", tags=["Семьи"])

@router.post("", response_model=FamilyCreateResponse)
async def create_family(name:str = Annotated[FamilyCreate, Depends()]):
    family_id = await Repository.create_family(name)
    return FamilyCreateResponse(
        message="Семья успешно создана",
        family_id=family_id
    )

@router.get("/{family_id}", response_model=list[FamilyUser])
async def find_family_members(family_id: int):
    members = await Repository.find_family_members(family_id)
    if not members:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Семья с таким ID не найдена")

    return members

@router.post("/{family_id}", response_model=FamilyUserAddResponse)
async def add_new_member(family_id: int, user_id: int):
    family = await Repository.find_family(user_id)

    if not family:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Такая семья или пользователь не существует")

    await Repository.add_member(family_id, user_id)

    return FamilyUserAddResponse(
        message="Пользователь успешно добавлен",
        id=user_id,
    )

@router.get("/{family_id}/recipes", response_model=list[Recipe])
async def get_family_recipes(user_id: int):
    recipes = await Repository.get_family_recipes(user_id)
    return recipes