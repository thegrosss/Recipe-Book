from app.core.database import async_session
from app.models import Family, Recipe
from app.models.family import FamilyUser

from sqlalchemy import select

from app.models.user import User


class Repository:
    @classmethod
    async def create_family(cls, name: str) -> int:
        async with async_session() as session:
            family = Family(name=name)

            session.add(family)

            await session.flush()
            await session.commit()

            return family.id

    @classmethod
    async def find_family(cls, user_id: int) -> int:
        async with async_session() as session:
            query = select(FamilyUser.family_id).where(FamilyUser.user_id == user_id)
            family = await session.execute(query)
            return family.scalar_one_or_none()

    @classmethod
    async def find_family_by_family_id(cls, family_id: int) -> int:
        async with async_session() as session:
            query = select(Family).filter_by(id=family_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def find_family_members(cls, family_id: int) -> list[User]:
        async with async_session() as session:
            query = select(FamilyUser.user_id).where(FamilyUser.family_id == family_id)
            result = await session.execute(query)
            members = result.scalars().all()

            if not members:
                return []

            query_users = select(User).where(User.id.in_(members))
            result = await session.execute(query_users)
            users = result.scalars().all()

            return users

    @classmethod
    async def add_member(cls, family_id: int, user_id: int) -> FamilyUser:
        async with async_session() as session:
            member = FamilyUser(family_id=family_id, user_id=user_id)
            session.add(member)

            await session.commit()
            return member

    @classmethod
    async def get_family_recipes(cls, user_id: int) -> list[Recipe]:
        async with async_session() as session:
            family_id = await Repository.find_family(user_id)

            if not family_id:
                return []

            members = await Repository.find_family_members(family_id)
            user_ids = [member.id for member in members]

            if not user_ids:
                return []

            recipe_query = select(Recipe).where(Recipe.owner_id.in_(user_ids))
            recipes = await session.execute(recipe_query)

            return recipes.scalars().all()