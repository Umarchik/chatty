from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities import Account

from app.application.services.account_service import AccountService
from app.presentation.web.dependencies import depends


router = APIRouter(prefix="/accounts", tags=["Аккаунты"])

AccountServiceDep = Annotated[AccountService, Depends(depends.get_accounts_service)]

@router.get("/", response_model=List[Account], summary="Получить все аккаунты")  
async def get_all_accounts(account_service: AccountServiceDep): 
    try:
        return await account_service.get_all_accounts()
    except:
        raise HTTPException(status_code=500, detail="Ошибка при получении аккаунтов")

@router.get("/{account_id}", response_model=Account, summary="Получить аккаунт по ID")
async def get_account_by_id(account_id: int, account_service: AccountServiceDep): 
    accounts = await account_service.get_all_accounts()
    for account in accounts:
        if account.id == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")

# Дополнительно можно добавить поиск по другим параметрам
@router.get("/search/{username}", response_model=Account, summary="Поиск по аккаунтам")
async def get_account_by_username(username: str, account_service: AccountServiceDep): 
       
    try:
        account = await account_service.get_account_by_username(username=username)
        if account:
            return account
    except:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")

@router.post("/", response_model=Account, summary="Создать аккаунт")
async def create_account(account_data: Account, account_service: AccountServiceDep): # type: ignore
    accounts = await account_service.get_all_accounts()
    if account_data.username:
        if any(acc.username == account_data.username for acc in accounts):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usename занят",
            )

    if account_data.phone:
        if any(acc.phone == account_data.phone for acc in accounts):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Телефон уже используется"
            )
    new_account =  await account_service.create_account(account_data)
    return new_account