from sqlalchemy import select

from app.schemas.user import User as User_schema
from app.models.user import User
from app.core.database import async_session

class Repository:
    @classmethod
    async def create_user(cls, user_data: User_schema) -> int:
        async with async_session() as session:
            user_dict = user_data.model_dump()
            user = User(**user_dict)

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