from fastapi import APIRouter, FastAPI
from app.schemas.recipe import RecipeAdd

api = FastAPI()

recipes = []

@api.post("/recipes")
async def create_recipe(recipe_data: RecipeAdd):
    recipe = recipe_data.model_dump()
    recipes.append(recipe)
    return recipe

@api.get("/recipes")
async def get_all_recipes():
    return recipes