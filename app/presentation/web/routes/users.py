from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.domain.enums.messenger_type import MessengerType

from app.application.dto.user_dto import UserResponseDTO, CreateUserDTO
from app.application.services.user_service import UserService
from app.application.services.account_service import AccountService
from app.presentation.web.dependencies import depends

router = APIRouter(prefix="/users", tags=["Пользователи"])

UserServiceDep = Annotated[UserService, Depends(depends.get_users_service)]
AccountServiceDep = Annotated[AccountService, Depends(depends.get_accounts_service)]


@router.get("/", response_model=List[UserResponseDTO], summary="Получить пользователей по мессенджеру")
async def get_all_users(
    messenger: MessengerType,
    user_service: UserServiceDep
):
    return await user_service.get_users_by_messenger_type(messenger)


@router.post("/", response_model=UserResponseDTO, summary="Создать пользователя")
async def create_user(
    user_data: CreateUserDTO,
    account_id: int,
    user_service: UserServiceDep,
    account_service: AccountServiceDep
):
    # Проверяем, есть ли аккаунт
    account = await account_service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")

    # Создаём пользователя
    return await user_service.create_user(user_data, account_id)
