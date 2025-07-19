from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from app.repository.recipe import Repository
from app.schemas.recipe import RecipeAdd, RecipeAddResponse

router = APIRouter(prefix="/recipes", tags=["Рецепты"])

@router.get("/all")
async def get_all_recipes():
    recipe = await Repository.get_all_recipes()

    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Рецепты не найдены")

    return recipe

@router.post("")
async def add_new_recipe(recipe_data: Annotated[RecipeAdd, Depends()],
                         owner_id: int): # owner_id потом заменить на id текущего через токен
    recipe_id = await Repository.add_new_recipe(recipe_data, owner_id=owner_id)

    return RecipeAddResponse(id=recipe_id)

