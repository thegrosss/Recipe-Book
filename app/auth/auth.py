from authx import AuthX, AuthXConfig

from app.core.config import settings
from app.repository.user import Repository
from app.core.security import verify_password

config = AuthXConfig(
    JWT_ALGORITHM=settings.ALGORITHM,
    JWT_SECRET_KEY=settings.SECRET_KEY,
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_TOKEN_LOCATION=["cookies"],
)

auth = AuthX(config=config)

async def authentication_user(phone_number: str, password: str):
    user = await Repository.find_user(phone_number=phone_number)

    if not user or not verify_password(password=password, hashed_password=user.password):
        return None
    else:
        return user