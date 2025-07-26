from fastapi import FastAPI

# Подключаем роутеры
from app.routers.user import router as users_router
from app.routers.recipes import router as recipes_router
from app.routers.family import router as family_router
from app.routers.auth import router as auth_router
from app.routers.shopping_list import router as shops_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(family_router)
app.include_router(shops_router)
