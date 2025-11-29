from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.domain.enums.messenger_type import MessengerType
from app.application.services.user_service import UserService
from app.presentation.web.dependencies import depends

router = APIRouter(prefix="/users", tags=["Пользователи"])

UserServiceDep = Annotated[UserService, Depends(depends.get_users_service)]

@router.get(path="/")
async def get_all_users(messenger: MessengerType, user_service: UserServiceDep):
    try:
        return await user_service.get_users_by_messenger_type(messenger)
    except:
        raise HTTPException(
            status_code=500,
            detail="Ошибка при получении пользователей"
        )