import logging
from typing import List, Optional, Tuple, Type

from app.domain.entities.account import Account
from app.application.dto.account_dto import (
    CreateAccountDTO, 
    UpdateAccountDTO, 
    AccountResponseDTO
)
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.application.mappers.account_mapper import AccountMapper
from app.application.mappers.user_mapper import UserMapper
from app.infrastructure.db.uow import UnitOfWork


class AccountService:
    def __init__(
        self,
        uow_class: Type[UnitOfWork],
        account_mapper: AccountMapper,
        user_mapper: UserMapper,
    ):
        self.uow_class = uow_class
        self.account_mapper = account_mapper
        self.user_mapper = user_mapper

    async def create_account(self, account_dto: CreateAccountDTO) -> AccountResponseDTO:
        """Создание нового аккаунта"""
        async with self.uow_class() as uow:
            try:
                account_entity = self.account_mapper.create_dto_to_entity(account_dto)
                saved_account = await uow.account.create(account_entity)
                return AccountResponseDTO.from_entity(saved_account)
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_account(self, account_id: int) -> Optional[AccountResponseDTO]:
        """Получение аккаунта по ID"""
        async with self.uow_class() as uow:
            account_entity = await uow.account.get(account_id)
            if account_entity:
                return AccountResponseDTO.from_entity(account_entity)
            return None

    async def get_account_by_username(self, username: str) -> Optional[AccountResponseDTO]:
        """Получение аккаунта по username"""
        async with self.uow_class() as uow:
            account_entity = await uow.account.get_by_username(username)
            if account_entity:
                return AccountResponseDTO.from_entity(account_entity)
            return None

    async def get_account_by_email(self, email: str) -> Optional[AccountResponseDTO]:
        """Получение аккаунта по email"""
        async with self.uow_class() as uow:
            account_entity = await uow.account.get_by_email(email)
            if account_entity:
                return AccountResponseDTO.from_entity(account_entity)
            return None

    async def get_all_accounts(self) -> List[AccountResponseDTO]:
        """Получение всех аккаунтов"""
        async with self.uow_class() as uow:
            account_entities = await uow.account.get_all()
            return [AccountResponseDTO.from_entity(account) for account in account_entities]

    async def update_account(
        self, 
        account_id: int, 
        update_dto: UpdateAccountDTO
    ) -> Optional[AccountResponseDTO]:
        """Обновление аккаунта"""
        async with self.uow_class() as uow:
            try:
                existing_account = await uow.account.get(account_id)
                if not existing_account:
                    return None

                update_data = update_dto.dict(exclude_unset=True)
                for field, value in update_data.items():
                    if hasattr(existing_account, field):
                        setattr(existing_account, field, value)

                updated_account = await uow.account.update(account_id, existing_account)
                if updated_account:
                    return AccountResponseDTO.from_entity(updated_account)
                return None
            except Exception as e:
                await uow.rollback()
                raise e

    async def delete_account(self, account_id: int) -> bool:
        """Удаление аккаунта"""
        async with self.uow_class() as uow:
            try:
                account = await uow.account.get(account_id)
                if not account:
                    return False

                success = await uow.account.delete(account_id)
                return success
            except Exception as e:
                await uow.rollback()
                raise e

    async def create_account_with_user(
        self, 
        account_dto: CreateAccountDTO, 
        user_dto: CreateUserDTO
    ) -> Tuple[AccountResponseDTO, UserResponseDTO]:
        """Создание аккаунта и пользователя в одной транзакции"""
        async with self.uow_class() as uow:
            try:
                account_db = await uow.account.get
                # Создаем аккаунт
                account_entity = self.account_mapper.create_dto_to_entity(account_dto)                
                saved_account = await uow.account.create(account_entity)              
                
                # Создаем пользователя с привязкой к аккаунту
                user_entity = self.user_mapper.create_dto_to_entity(user_dto, account_id=saved_account.id)
                saved_user = await uow.user.create(user_entity)
                
                return (
                    AccountResponseDTO.from_entity(saved_account),
                    UserResponseDTO.from_entity(saved_user)
                )
            except Exception as e:
                await uow.rollback()
                raise e
            
    async def get_account_by_user_external_id(self, external_id: str):
        async with self.uow_class() as uow:
            account_entity = await uow.account.get_by_user_external_id(external_id)
            if account_entity:
                return AccountResponseDTO.from_entity(account_entity)
            return None