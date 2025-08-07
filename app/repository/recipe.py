from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import async_session
from app.models.recipe import Recipe
from app.models.user import User
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
    async def get_user_recipes(cls, user_id: int) -> list[Recipe]:
        async with async_session() as session:
            result = await session.execute(
                select(User)
                .where(user_id == User.id)
                .options(selectinload(User.recipes))
            )
            user = result.scalars().first()
            return user.recipes if user else []

    @classmethod
    async def add_new_recipe(cls, recipe_data: RecipeAdd, owner_id: int) -> int:
        async with async_session() as session:
            recipe_dict = recipe_data.model_dump()
            recipe = Recipe(**recipe_dict)

            owner = await session.get(User, owner_id)
            owner.recipes.append(recipe)

            session.add(recipe)
            await session.flush()
            await session.commit()

            return recipe.id

    @classmethod
    async def like_recipe(cls, user_id: int, recipe_id: int):
        async with async_session() as session:
            user = await session.get(User, user_id)
            recipe = await session.get(Recipe, recipe_id)

            if not recipe or recipe in user.recipes:
                return False

            user.recipes.append(recipe)
            await session.commit()
            return True

    @classmethod
    async def unlike_recipe(cls, user_id: int, recipe_id: int):
        async with async_session() as session:
            user = await session.get(User, user_id)
            recipe = await session.get(Recipe, recipe_id)

            if not recipe or not recipe in user.recipes:
                return False

            user.recipes.remove(recipe)
            await session.commit()
            return True

    @classmethod
    async def get_recipes_by_tag(cls, tag: str) -> list[Recipe]:
        async with async_session() as session:
            query = select(Recipe).where(Recipe.tag.contains(tag))
            recipes = await session.execute(query)

            return recipes.scalars().all()

    @classmethod
    async def get_recipes_by_name(cls, name: str):
        async with async_session() as session:
            name_list = "".join([x.upper() for x in name.split() if len(x) > 2])
            query = select(Recipe).where(Recipe.content.contains(name_list))

            recipes = await session.execute(query)

            return recipes.scalars().all()