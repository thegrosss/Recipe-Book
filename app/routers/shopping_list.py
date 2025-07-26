from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.shopping_list import ShoppingListAdd, ShoppingListAddResponse, ShoppingListGet
from app.repository.shopping_list import Repository
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/shops", tags=["Списки продуктов"])

@router.post("", response_model=ShoppingListAddResponse)
async def create_new_list(list_data: Annotated[ShoppingListAdd, Depends()],
                          owner: User = Depends(get_current_user)):
    sh_list_id = await Repository.create_list(owner.id, list_data.title, list_data.items)

    return ShoppingListAddResponse(id=sh_list_id)

@router.get("/me", response_model=list[ShoppingListGet])
async def get_user_shop_lists(owner: User = Depends(get_current_user)):
    sh_lists = await Repository.get_user_lists(owner.id)

    if not sh_lists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Списки продуктов не найдены")

    return sh_lists