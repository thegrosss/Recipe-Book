from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.repository.recipe import Repository as recipe_rep
from app.repository.user import Repository as user_rep

from app.schemas.recipe import RecipeAdd, RecipeAddResponse, Recipe
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/recipes", tags=["Рецепты"])

@router.post("", response_model=RecipeAddResponse)
async def add_new_recipe(recipe_data: Annotated[RecipeAdd, Depends()],
                         owner: User = Depends(get_current_user)):
    recipe_id = await recipe_rep.add_new_recipe(recipe_data, owner_id=owner.id)

    return RecipeAddResponse(id=recipe_id)

@router.get("/me", response_model=list[Recipe])
async def get_user_recipe(owner: User = Depends(get_current_user)):
    user = await user_rep.find_user(id=owner.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким ID не найден")

    recipes = await user_rep.get_user_recipes(user_id=owner.id)

    if not recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="У этого пользователя нет рецептов")

    return recipes

@router.get("/all", response_model=list[Recipe])
async def get_all_recipes():
    recipe = await recipe_rep.get_all_recipes()

    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецепты не найдены")

    return recipe