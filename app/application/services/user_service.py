from typing import List, Optional, Type
from app.domain.entities.user import User
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.application.mappers.user_mapper import UserMapper
from app.infrastructure.db.uow import UnitOfWork
from app.domain.enums.messenger_type import MessengerType


class UserService:
    def __init__(
        self,
        uow_class: Type[UnitOfWork],
        user_mapper: UserMapper,
    ):
        self.uow_class = uow_class
        self.user_mapper = user_mapper

    async def create_user(self, user_dto: CreateUserDTO, account_id: int) -> UserResponseDTO:
        """Создание пользователя"""
        async with self.uow_class() as uow:
            try:
                user_entity = self.user_mapper.create_dto_to_entity(dto=user_dto, account_id=account_id)
                saved_user = await uow.user.create(user_entity)
                return UserResponseDTO.from_entity(saved_user)
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_user(self, user_id: int) -> Optional[UserResponseDTO]:
        """Получение пользователя по ID"""
        async with self.uow_class() as uow:
            user_entity = await uow.user.get(user_id)
            if user_entity:
                return UserResponseDTO.from_entity(user_entity)
            return None

    async def get_user_by_external_id(
        self, 
        external_id: str, 
        messenger_type: MessengerType
    ) -> Optional[UserResponseDTO]:
        """Получение пользователя по external_id и messenger_type"""
        async with self.uow_class() as uow:
            user_entity = await uow.user.get_by_external_id(
                external_id=external_id,
                messenger_type=messenger_type.value
            )
            if user_entity:
                return UserResponseDTO.from_entity(user_entity)
            return None

    async def get_users_by_account_id(self, account_id: int) -> List[UserResponseDTO]:
        """Получение пользователей по account_id"""
        async with self.uow_class() as uow:
            user_entities = await uow.user.get_by_account_id(account_id)
            return [UserResponseDTO.from_entity(user) for user in user_entities]

    async def get_users_by_messenger_type(self, messenger_type: MessengerType) -> List[UserResponseDTO]:
        """Получение пользователей по типу мессенджера"""
        async with self.uow_class() as uow:
            user_entities = await uow.user.get_by_messenger_type(messenger_type)
            return [UserResponseDTO.from_entity(user) for user in user_entities]

    async def update_user(
        self, 
        user_id: int, 
        update_dto: UpdateUserDTO
    ) -> Optional[UserResponseDTO]:
        """Обновление пользователя"""
        async with self.uow_class() as uow:
            try:
                existing_user = await uow.user.get(user_id)
                if not existing_user:
                    return None

                update_data = update_dto.dict(exclude_unset=True)
                for field, value in update_data.items():
                    if hasattr(existing_user, field):
                        setattr(existing_user, field, value)

                updated_user = await uow.user.update(user_id, existing_user)
                if updated_user:
                    return UserResponseDTO.from_entity(updated_user)
                return None
            except Exception as e:
                await uow.rollback()
                raise e

    async def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        async with self.uow_class() as uow:
            try:
                user = await uow.user.get(user_id)
                if not user:
                    return False

                success = await uow.user.delete(user_id)
                return success
            except Exception as e:
                await uow.rollback()
                raise e

    async def get_or_create_user_from_telegram(
        self,
        telegram_user,
        account_id: int
    ) -> UserResponseDTO:
        """Получение или создание пользователя для Telegram"""
        async with self.uow_class() as uow:
            try:
                # Пытаемся найти существующего пользователя
                existing_user = await uow.user.get_by_external_id(
                    external_id=str(telegram_user.id),
                    messenger_type=MessengerType.TELEGRAM.value
                )
                
                if existing_user:
                    return UserResponseDTO.from_entity(existing_user)
                
                # Создаем нового пользователя
                user_dto = CreateUserDTO(
                    external_id=str(telegram_user.id),
                    messenger_type=MessengerType.TELEGRAM,
                    username=telegram_user.username,
                    first_name=telegram_user.first_name,
                    last_name=telegram_user.last_name,
                )
                
                user_entity = self.user_mapper.create_dto_to_entity(user_dto, account_id)
                saved_user = await uow.user.create(user_entity)
                return UserResponseDTO.from_entity(saved_user)
                
            except Exception as e:
                await uow.rollback()
                raise e