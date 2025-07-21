from app.auth.auth import auth, config
from fastapi import Request, HTTPException, status, Depends

from datetime import datetime, timezone
from app.repository.user import Repository

async def get_token(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не найден")
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = auth._decode_token(token=token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен не валидный")

    exp = payload.exp
    if not exp or exp < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Время действия токена истекло")

    user_id = payload.sub

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь с таким номером телефона не найден")

    user = await Repository.find_user(id=int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return user