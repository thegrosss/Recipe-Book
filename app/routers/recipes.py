from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.repository.recipe import Repository

from app.schemas.recipe import RecipeAdd, RecipeAddResponse, Recipe
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/recipes", tags=["Рецепты"])

@router.post("", response_model=RecipeAddResponse)
async def add_new_recipe(recipe_data: Annotated[RecipeAdd, Depends()],
                         owner: User = Depends(get_current_user)):
    recipe_id = await Repository.add_new_recipe(recipe_data, owner_id=owner.id)

    return RecipeAddResponse(id=recipe_id)

@router.post("/{recipe_id}/like")
async def like_recipe(recipe_id: int,
                      user: User = Depends(get_current_user)):
    success = await Repository.like_recipe(user_id=user.id, recipe_id=recipe_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Рецепт уже в избранном или не существует"
        )
    return {"message" : "Рецепт успешно добавлен в избранные"}

@router.post("/{recipe_id}/unlike")
async def unlike_recipe(recipe_id: int,
                        user: User = Depends(get_current_user)):
    success = await Repository.unlike_recipe(user_id=user.id, recipe_id=recipe_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Рецепт уже не в избранном или не существует"
        )
    return {"message" : "Рецепт успешно удален из избранных"}

@router.get("/me", response_model=list[Recipe])
async def get_user_recipe(owner: User = Depends(get_current_user)):
    recipes = await Repository.get_user_recipes(user_id=owner.id)

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецептов не найдено")

    return recipes

@router.get("/all", response_model=list[Recipe])
async def get_all_recipes():
    recipes = await Repository.get_all_recipes()

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецепты не найдены")

    return recipes

@router.get("/category", response_model=list[Recipe])
async def get_recipe_by_tag(tag: str):
    recipes = await Repository.get_recipes_by_tag(tag.capitalize())

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецепты не найдены")

    return recipes

@router.get("/other")
async def get_recipes_by_name(name: str):
    recipes = await Repository.get_recipes_by_name(name)

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецепты не найдены")

    return recipes