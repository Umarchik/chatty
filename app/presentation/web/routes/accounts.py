from typing import List
from fastapi import APIRouter, HTTPException, status
from app.domain.entities import Account
from datetime import datetime


router = APIRouter(prefix="/accounts", tags=["Аккаунты"])

# Данные
accounts = []

@router.get("/", response_model=List[Account], summary="Получить все аккаунты")  # Более RESTful путь
async def get_all_accounts():
    return accounts

@router.get("/{account_id}", response_model=Account, summary="Получить аккаунт по ID")
async def get_account_by_id(account_id: int):
    for account in accounts:
        if account.id == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")

# Дополнительно можно добавить поиск по другим параметрам
@router.get("/search/{username}", response_model=Account, summary="Поиск по аккаунтам")
async def get_account_by_username(phone: str):
    for account in accounts:
        if account.phone == phone:
            return account
    raise HTTPException(status_code=404, detail="Аккаунт не найден")

@router.post("/", response_model=Account, summary="Создать аккаунт")
async def create_account(account_data: Account):
    max_id = 0
    if accounts:
        max_id = max(account.id for account in accounts)
    new_id = max_id+1

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
        
    # Создаем новый аккаунт
    now = datetime.now()
    new_account = Account(
        id=new_id,
        username=account_data.username,
        email=account_data.email,
        phone=account_data.phone,
        first_name=account_data.first_name,
        last_name=account_data.last_name,
        created_at=now,
        updated_at=now,
        users=[]
    )
    
    # Добавляем в список
    accounts.append(new_account)
    
    return new_account