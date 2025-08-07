from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.deps import get_current_user
from app.repository.user import Repository
from app.core.config import user_tokens

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.get("/me/token")
async def get_user_token(id: int):
    return user_tokens[id]

@router.get("/all")
async def find_user(phone_number: str = None, id: int = None):
    if id:
        user = await Repository.find_user(id=id)
        return user
    elif phone_number:
        user = await Repository.find_user(phone_number=phone_number)
        return user
    else:
        return None