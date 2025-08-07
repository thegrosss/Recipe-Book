from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.repository.family import Repository as family_rep
from app.repository.user import Repository as user_rep

from app.schemas.family import FamilyCreate, FamilyCreateResponse, FamilyUserAddResponse, FamilyUser
from app.schemas.recipe import Recipe

from app.models.user import User

from app.core.deps import get_current_user

router = APIRouter(prefix="/families", tags=["Семьи"])

@router.post("", response_model=FamilyCreateResponse)
async def create_family(name:str = Annotated[FamilyCreate, Depends()],
                        owner: User = Depends(get_current_user)):
    user_family = await family_rep.find_family_by_user_id(owner.id)
    if user_family:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="У вас уже есть семья")

    family_id = await family_rep.create_family(name, owner.id)

    return FamilyCreateResponse(
        message="Семья успешно создана",
        family_id=family_id
    )

@router.get("")
async def find_family_by_user_id(owner: User = Depends(get_current_user)):
    user_family = await family_rep.find_family_by_user_id(owner.id)
    return user_family

@router.get("/members", response_model=list[FamilyUser])
async def find_family_members(user: User = Depends(get_current_user)):
    family_id = await family_rep.find_family_by_user_id(user_id=user.id)

    if not family_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Вы не состоите в семье")

    members = await family_rep.find_family_members(family_id)

    if not members:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="В этой семье нет пользователей")

    return members

@router.post("/members", response_model=FamilyUserAddResponse)
async def add_new_member(new_member_id: int,
                         user: User = Depends(get_current_user)):
    if new_member_id == user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Вы не можете добавить в семью самого себя")

    new_member = await user_rep.find_user(id=new_member_id)
    if not new_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Такого пользователя не существует")

    family = await family_rep.find_family_by_user_id(user_id=user.id)

    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Вы не состоите в семье, поэтому "
                             "не можете добавить нового пользователя")

    member_family = await family_rep.find_family_by_user_id(user_id=new_member_id)

    if member_family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Этот пользователь уже состоит в семье")

    await family_rep.add_member(new_member_id, user.id)

    new_member = await user_rep.find_user(id=new_member_id)

    return FamilyUserAddResponse(
        message=f"Пользователь {new_member.first_name} успешно добавлен",
        id=new_member_id,
    )

@router.get("/recipes", response_model=list[Recipe])
async def get_family_recipes(user: User = Depends(get_current_user)):

    family = await family_rep.find_family_by_user_id(user_id=user.id)

    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Вы не состоите в семье, поэтому "
                             "не можете посмотреть семейные рецепты")

    recipes = await family_rep.get_family_recipes(user.id)

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail="Рецептов не найдено")
    return recipes