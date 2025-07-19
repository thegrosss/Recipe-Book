from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_gb_url

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(get_gb_url())
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)