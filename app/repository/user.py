from app.schemas.user import UserRegister

from app.models.user import User
from app.models.recipe import Recipe

from app.core.database import async_session
from app.core.security import get_password_hash

from sqlalchemy import select

class Repository:
    @classmethod
    async def create_user(cls, user_data: UserRegister) -> int:
        async with async_session() as session:
            user_dict = user_data.model_dump()
            user = User(**user_dict)

            user_data.password = get_password_hash(user_data.password)

            session.add(user)

            await session.flush()
            await session.commit()

            return user.id

    @classmethod
    async def find_user(cls, **filters) -> User:
        async with async_session() as session:
            query = select(User).filter_by(**filters)
            user = await session.execute(query)
            return user.scalar_one_or_none()

    @classmethod
    async def get_user_recipes(cls, user_id: int) -> list[Recipe]:
        async with async_session() as session:
            query = select(Recipe).filter_by(owner_id=user_id)
            recipes = await session.execute(query)

            return recipes.scalars().all()