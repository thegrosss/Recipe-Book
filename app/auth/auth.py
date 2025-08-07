from authx import AuthX, AuthXConfig
from app.core.config import settings
from app.repository.user import Repository

config = AuthXConfig(
    JWT_ALGORITHM=settings.ALGORITHM,
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_TOKEN_LOCATION=["cookies"],
)

auth = AuthX(config=config)

async def authentication_user(phone_number: str):
    user = await Repository.find_user(phone_number=phone_number)

    if not user:
        return None
    else:
        return user