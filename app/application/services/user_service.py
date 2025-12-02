from typing import List, Optional, Type
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
        async with self.uow_class() as uow:

            # Проверяем существование аккаунта
            account = await uow.account.get(account_id)
            if not account:
                raise ValueError("Указанный аккаунт не найден")

            # Создать entity
            user_entity = self.user_mapper.from_create_dto(user_dto, account_id)

            # Сохранить
            saved_user = await uow.user.create(user_entity)

            return self.user_mapper.to_response_dto(saved_user)

    async def get_user(self, user_id: int) -> Optional[UserResponseDTO]:
        async with self.uow_class() as uow:
            entity = await uow.user.get(user_id)
            return self.user_mapper.to_response_dto(entity) if entity else None

    async def get_user_by_external_id(
        self,
        external_id: str,
        messenger_type: MessengerType
    ) -> Optional[UserResponseDTO]:
        async with self.uow_class() as uow:
            entity = await uow.user.get_by_external_id(
                external_id=external_id,
                messenger_type=messenger_type.value
            )
            return self.user_mapper.to_response_dto(entity) if entity else None

    async def get_users_by_account_id(self, account_id: int) -> List[UserResponseDTO]:
        async with self.uow_class() as uow:
            entities = await uow.user.get_by_account_id(account_id)
            return [self.user_mapper.to_response_dto(e) for e in entities]

    async def get_users_by_messenger_type(self, messenger_type: MessengerType) -> List[UserResponseDTO]:
        async with self.uow_class() as uow:
            entities = await uow.user.get_by_messenger_type(messenger_type.value)
            return [self.user_mapper.to_response_dto(e) for e in entities]

    async def update_user(self, user_id: int, update_dto: UpdateUserDTO) -> Optional[UserResponseDTO]:
        async with self.uow_class() as uow:
            existing = await uow.user.get(user_id)
            if not existing:
                return None

            updates = update_dto.dict(exclude_unset=True)

            updated = await uow.user.update(user_id, updates)
            return self.user_mapper.to_response_dto(updated) if updated else None

    async def delete_user(self, user_id: int) -> bool:
        async with self.uow_class() as uow:
            existing = await uow.user.get(user_id)
            if not existing:
                return False

            return await uow.user.delete(user_id)

    async def get_or_create_user_from_telegram(self, tg_user, account_id: int) -> UserResponseDTO:
        async with self.uow_class() as uow:

            # Проверяем аккаунт
            account = await uow.account.get(account_id)
            if not account:
                raise ValueError("Аккаунт не найден")

            # Ищем пользователя
            existing = await uow.user.get_by_external_id(
                external_id=str(tg_user.id),
                messenger_type=MessengerType.TELEGRAM.value
            )

            if existing:
                return self.user_mapper.to_response_dto(existing)

            # Создаём DTO
            dto = CreateUserDTO(
                external_id=str(tg_user.id),
                messenger_type=MessengerType.TELEGRAM,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
            )

            # Маппинг + сохранение
            entity = self.user_mapper.from_create_dto(dto, account_id)
            saved = await uow.user.create(entity)

            return self.user_mapper.to_response_dto(saved)
