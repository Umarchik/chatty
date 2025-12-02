from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dto.account_dto import CreateAccountDTO, AccountResponseDTO
from app.application.services.account_service import AccountService
from app.presentation.web.dependencies import depends


router = APIRouter(prefix="/accounts", tags=["Аккаунты"])

AccountServiceDep = Annotated[AccountService, Depends(depends.get_accounts_service)]

@router.get("/", response_model=List[AccountResponseDTO], summary="Получить все аккаунты")  
async def get_all_accounts(account_service: AccountServiceDep): 
        return await account_service.get_all_accounts()
    

@router.get("/{account_id}", response_model=AccountResponseDTO, summary="Получить аккаунт по ID")
async def get_account_by_id(account_id: int, account_service: AccountServiceDep): 
        account = await account_service.get_account(account_id=account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

        

# Дополнительно можно добавить поиск по другим параметрам
@router.get("/search/{username}", response_model=AccountResponseDTO, summary="Поиск по аккаунтам")
async def get_account_by_username(username: str, account_service: AccountServiceDep): 
       
        account = await account_service.get_account_by_username(username=username)
        if not account:
            raise HTTPException(status_code=404, detail="Аккаунт не найден")
        return account
        

@router.post("/", response_model=AccountResponseDTO, summary="Создать аккаунт")
async def create_account(account_data: CreateAccountDTO, account_service: AccountServiceDep): # type: ignore
    if account_data.username:
        existing = await account_service.get_account_by_username(account_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username занят",
            )
    new_account =  await account_service.create_account(account_data)
    return new_account