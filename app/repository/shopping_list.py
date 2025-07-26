from app.core.database import async_session
from app.models.shopping_list import ShoppingList

from sqlalchemy import select

class Repository:
    @classmethod
    async def create_list(cls, owner_id: int, title: str, items: str) -> int:
        async with async_session() as session:
            sh_list =  ShoppingList(owner_id=owner_id, title=title, items=items)
            session.add(sh_list)
            await session.flush()
            await session.commit()

            return sh_list.id

    @classmethod
    async def get_user_lists(cls, owner_id: int) -> list[ShoppingList]:
        async with async_session() as session:
            query = select(ShoppingList).filter_by(owner_id=owner_id)
            lists = await session.execute(query)

            return lists.scalars().all()