from sqlalchemy import select

from app.core.database import async_session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeAdd


class Repository:
    @classmethod
    async def find_recipe(cls, **filters) -> Recipe | list[Recipe]:
        async with async_session() as session:
            query = select(Recipe).filter_by(**filters)
            recipies = await session.execute(query)
            return recipies.scalars().all()

    @classmethod
    async def get_all_recipes(cls):
        async with async_session() as session:
            query = select(Recipe)
            recipes = await session.execute(query)

            return recipes.scalars().all()

    @classmethod
    async def add_new_recipe(cls, recipe_data: RecipeAdd, owner_id: int) -> int:
        async with async_session() as session:
            recipe_dict = recipe_data.model_dump()
            recipe = Recipe(**recipe_dict, owner_id=owner_id)

            session.add(recipe)

            await session.flush()
            await session.commit()

            return recipe.id
