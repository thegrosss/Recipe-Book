from fastapi import FastAPI

# Подключаем роутеры
from app.routers.user import router as users_router
from app.routers.recipes import router as recipes_router
from app.routers.family import router as family_router

app = FastAPI()
app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(family_router)