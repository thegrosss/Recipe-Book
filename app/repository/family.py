from app.core.database import async_session

from app.models.family import Family, FamilyUser
from app.models.recipe import Recipe
from app.models.user import User

from sqlalchemy import select

class Repository:
    @classmethod
    async def create_family(cls, name: str, user_id: int) -> int:
        async with async_session() as session:
            family = Family(name=name)

            session.add(family)

            await session.flush()
            await session.commit()

            owner = FamilyUser(user_id=user_id, family_id=family.id)
            session.add(owner)

            await session.flush()
            await session.commit()

            return family.id

    @classmethod
    async def find_family_by_user_id(cls, user_id: int) -> int:
        async with async_session() as session:
            query = select(FamilyUser.family_id).where(FamilyUser.user_id == user_id)
            family = await session.execute(query)
            return family.scalars().first()

    @classmethod
    async def find_family_by_family_id(cls, family_id: int) -> int:
        async with async_session() as session:
            query = select(Family.id).where(Family.id == family_id)
            result = await session.execute(query)

            return result.scalars().first()

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
    async def add_member(cls,new_member_id: int, owner_id: int) -> FamilyUser:
        async with async_session() as session:
            family_id = await Repository.find_family_by_user_id(owner_id)
            member = FamilyUser(user_id=new_member_id, family_id=family_id)

            session.add(member)
            await session.commit()

            return member

    @classmethod
    async def get_family_recipes(cls, user_id: int) -> list[Recipe]:
        async with async_session() as session:
            family_id = await Repository.find_family_by_user_id(user_id)

            if not family_id:
                return []

            members = await Repository.find_family_members(family_id)
            user_ids = [member.id for member in members]

            if not user_ids:
                return []

            recipe_query = select(Recipe).where(Recipe.owner_id.in_(user_ids))
            recipes = await session.execute(recipe_query)

            return recipes.scalars().all()