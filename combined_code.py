
# --- main.py ---
import asyncio
import logging
import uvicorn
from app.core.config.logging import setup_logging
from app.core.config.settings import Config
from app.presentation.web.web_app import create_app


async def main():
    config = Config.load()
    log_level = logging.DEBUG if config.env.debug else logging.INFO
    setup_logging(level=log_level)
    logging.info(f"🚀 Приложение запущено в режиме {config.env.env.upper()} (debug={config.env.debug})")

    # создаём FastAPI-приложение (бот + веб)
    app = await create_app(config)
    

    # Настройка uvicorn
    uvicorn_config = uvicorn.Config(
        app=app,
        host=config.web.host,
        port=config.web.port,
        log_level=log_level,
        log_config=None,
        reload=config.env.debug,
        use_colors=False,  
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("❌ Сервер остановлен вручную")



# --- combined_code.py ---



# --- sb.py ---
import os

def combine_python_files(root_dir, output_file, excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = {'venv', '__pycache__', '.git', 'env', 'logs', 'alembic', '.ini', 'sb.py'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            # Исключаем указанные директории
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    # Записываем комментарий с именем файла
                    outfile.write(f'\n# --- {relative_path} ---\n')
                    
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    outfile.write('\n\n')

if __name__ == '__main__':
    project_dir = '.'  # Текущая директория (можно изменить)
    output_filename = 'combined_code.py'
    combine_python_files(project_dir, output_filename)


# --- app/domain/enums/chat_member_status.py ---
from enum import Enum


class ChatMemerStatus(Enum):
    
    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"

    @classmethod
    def get_by_value(cls, value: str):
        for status in cls:
            if status.value == value:
                return status
        raise ValueError(f"Unkown status: {value}")



# --- app/domain/enums/message_status.py ---
from enum import Enum


class MessageStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"


# --- app/domain/enums/messenger_type.py ---
from enum import Enum


class MessengerType(str, Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    MAX = "MAX"
    VK = "vk"



# --- app/domain/enums/message_type.py ---
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    VOICE = "voice"
    DOCUMENT = "document"
    STICKER = "sticker"
    LOCATION = "location"
    CONTACT = "contact"
    POLL = "poll"
    ANIMATION = "animation"
    
    @classmethod
    def get_by_value(cls, value: str):
        for msg_type in cls:
            if msg_type.value == value:
                return msg_type
        return cls.TEXT


# --- app/domain/enums/chat_type.py ---
from enum import Enum


class ChatType(str, Enum):
    PRIVATE = "privite"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
    


# --- app/domain/enums/__init__.py ---
from .chat_type import ChatType
from .chat_member_status import ChatMemerStatus
from .message_type import MessageType
from .messenger_type import MessengerType
from .message_status import MessageStatus


__all__ = (
    "ChatType",
    "ChatMemerStatus",
    "MessageType",
    "MessengerType",
    "MessageStatus"
)



# --- app/domain/entities/account.py ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class Account(BaseModel):
    """Основной аккаунт пользователя, объединяющий профили из разных мессенджеров"""
    
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    created_at: Optional[datetime] = None
    
    def get_full_name(self) -> str:
        names = [self.first_name, self.last_name]
        return " ".join([name for name in names if name])



# --- app/domain/entities/chat.py ---
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..enums import ChatType


class Chat(BaseModel):
    id: int
    external_id: str
    messenger_type: str
    title: Optional[str] = None
    chat_type: ChatType
    created_at: datetime
    
    def is_group_chat(self) -> bool:
        return self.chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]


# --- app/domain/entities/message.py ---
from typing import TYPE_CHECKING
from pydantic import BaseModel
from datetime import datetime

from ..enums import MessengerType, MessageStatus
from app.domain.entities.chat import Chat
from app.domain.entities.user import User


class Message(BaseModel):
    id: int  
    external_id: str  
    messenger_type: MessengerType
    text: str
    user: User  
    chat: Chat  
    status: MessageStatus
    created_at: datetime
    
    def is_moderated(self) -> bool:
        return self.status != MessageStatus.PENDING
    
    def is_telegram_message(self) -> bool:
        return self.messenger_type == MessengerType.TELEGRAM
    
    def can_be_edited(self) -> bool:
        return self.messenger_type in [MessengerType.TELEGRAM, MessengerType.DISCORD]
    
    def get_messenger_identity(self) -> str:
        """Возвращает идентификатор сообщения в контексте мессенджера"""
        return f"{self.messenger_type}:{self.external_id}"


# --- app/domain/entities/user.py ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.entities.account import Account
from ..enums.messenger_type import MessengerType


class User(BaseModel):
    id: Optional[int] = None
    external_id: str
    messenger_type: MessengerType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account_id: int
    created_at: datetime
    
    def get_full_name(self) -> str:
        names = [self.first_name, self.last_name]
        return " ".join([name for name in names if name])

    def get_account(self) -> Optional[Account]:
        pass
    


# --- app/domain/entities/__init__.py ---
from .account import Account
from .user import User
from .chat import Chat
from .message import Message


__all__ = (
    "Account",
    "User",
    "Chat",
    "Message",
)



# --- app/domain/repositories/account.py ---
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.account import Account
from .base import BaseRepository

class AccountRepository(BaseRepository[Account], ABC):
    """Интерфейс репозитория аккаунтов"""
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[Account]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Account]:
        pass
    


# --- app/domain/repositories/interfaces.py ---
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)  # Domain Entity
M = TypeVar('M')  # Database Model

class IEntityMapper(ABC, Generic[T, M]):
    """Интерфейс для мапперов Entity ↔ Database Model"""
    
    @abstractmethod
    def to_entity(self, model: M) -> Optional[T]:
        """Преобразование Database Model → Domain Entity"""
        pass
    
    @abstractmethod
    def to_model(self, entity: T) -> M:
        """Преобразование Domain Entity → Database Model"""
        pass


# --- app/domain/repositories/user.py ---
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User
from .base import BaseRepository

class UserRepository(BaseRepository[User], ABC):
    """Интерфейс репозитория пользователей"""
    
    @abstractmethod
    async def get_by_external_id(self, external_id: str, messenger_type: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_account_id(self, account_id: int) -> List[User]:
        pass
    


# --- app/domain/repositories/base.py ---
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)  # Domain Entity

class BaseRepository(ABC, Generic[T]):
    """Абстрактный базовый репозиторий - только интерфейсы"""
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    async def update(self, id: int, entity: T) -> Optional[T]:
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass


# --- app/domain/repositories/__init__.py ---
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.user import UserRepository


__all__ = (
    "AccountRepository",
    "UserRepository",
)


# --- app/application/__init__.py ---



# --- app/application/dto/message_dto.py ---
from datetime import datetime
from pydantic import BaseModel

from app.domain.entities.chat import Chat
from app.domain.entities.message import Message
from app.domain.entities.user import User
from app.domain.enums.message_status import MessageStatus
from app.domain.enums.messenger_type import MessengerType


class CreateMessageDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    text: str
    user: User
    chat: Chat

class UpdateMessageDTO(BaseModel):
    status: MessageStatus

class MessageResponseDTO(BaseModel):
    id: int
    external_id: str
    messenger_type: MessengerType
    text: str
    user: User
    chat: Chat
    status: MessageStatus
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageResponseDTO":
        return cls(
            id = message.id,
            external_id = message.external_id,
            messenger_type = message.messenger_type,
            text = message.text,
            user = message.user,
            chat = message.chat,
            status = message.status,
            created_at = message.created_at
        )


# --- app/application/dto/user_dto.py ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from redis import int_or_str

from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.enums.messenger_type import MessengerType


class CreateUserDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str]  = None
    account_id: int


class UpdateUserDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account_id: int_or_str

class UserResponseDTO(BaseModel):
    id: int
    external_id: str
    username: Optional[str] = None
    first_name: Optional[str]= None
    last_name: Optional[str] = None
    account_id: int
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserResponseDTO":
        return cls(
            id = user.id,
            external_id = user.external_id,
            messenger_type = user.messenger_type,
            username = user.username,
            first_name = user.first_name,
            last_name = user.last_name,
            account_id = user.account_id,
            created_at = user.created_at
        )




# --- app/application/dto/chat_dto.py ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.entities.chat import Chat
from app.domain.enums.chat_type import ChatType
from app.domain.enums.messenger_type import MessengerType


class CreateChatDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    title: Optional[str] = None
    chat_type: ChatType

class UpdateChatDTO(BaseModel):
    title: Optional[str] = None

class ChatResponseDTO(BaseModel):
    id: int
    external_id: str
    messenger_type: MessengerType
    title: Optional[str] = None
    chat_type: ChatType
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatResponseDTO":
        return cls(
            id = chat.id,
            external_id = chat.external_id,
            messenger_type = chat.messenger_type,
            title = chat.title,
            chat_type = chat.chat_type,
            created_at = chat.created_at,
        )


# --- app/application/dto/account_dto.py ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.entities.account import Account


class CreateAccountDTO(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str]  = None

class UpdateAccountDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AccountResponseDTO(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str]= None
    last_name: Optional[str] = None
    created_at: datetime

    @classmethod
    def from_entity(cls, account: Account) -> "AccountResponseDTO":
        return cls(
            id = account.id,
            email = account.email,
            username = account.username,
            first_name = account.first_name,
            last_name = account.last_name,
            created_at = account.created_at
        )




# --- app/application/di/container.py ---
from app.infrastructure.db.mappers.account_mapper import AccountDbMapper
from app.infrastructure.db.mappers.user_mapper import UserDbMapper
from app.infrastructure.db.uow import UnitOfWork
from app.application.mappers.account_mapper import AccountMapper
from app.application.mappers.user_mapper import UserMapper
from app.application.services.account_service import AccountService
from app.application.services.user_service import UserService

class Container:
    """Контейнер для dependency injection"""
    
    def __init__(self):
        self._uow_class = UnitOfWork
        self._account_mapper = AccountMapper()
        self._account_db_mapper = AccountDbMapper()
        self._user_mapper = UserMapper()
        self._user_db_mapper = UserDbMapper()
    
    def account_service(self) -> AccountService:
        """Создание сервиса аккаунтов с зависимостями"""
        return AccountService(
            uow_class=self._uow_class,
            account_mapper=self._account_mapper,
            account_db_mapper = self._account_db_mapper,
            user_mapper=self._user_mapper,
            user_db_mapper = self._user_db_mapper
        )
    
    def user_service(self) -> UserService:
        """Создание сервиса пользователей с зависимостями"""
        return UserService(
            uow_class=self._uow_class,
            user_mapper=self._user_mapper,
            user_db_mapper = self._user_db_mapper,
        )


# --- app/application/services/account_service.py ---
from typing import List, Optional, Tuple, Type
from datetime import datetime

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
                # Создаем аккаунт
                account_entity = self.account_mapper.create_dto_to_entity(account_dto)
                saved_account = await uow.account.create(account_entity)
                
                # Создаем пользователя с привязкой к аккаунту
                user_entity = self.user_mapper.create_dto_to_entity(user_dto)
                
                saved_user = await uow.user.create(user_entity)
                
                return (
                    AccountResponseDTO.from_entity(saved_account),
                    UserResponseDTO.from_entity(saved_user)
                )
            except Exception as e:
                await uow.rollback()
                raise e
            


# --- app/application/services/user_service.py ---
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
                user_entity = self.user_mapper.create_dto_to_entity(user_dto, account_id)
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
            user_entities = await uow.user.get_by_messenger_type(messenger_type.value)
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


# --- app/application/mappers/user_mapper.py ---
from datetime import datetime
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.domain.entities.user import User


class UserMapper:
    @staticmethod
    def create_dto_to_entity(dto: CreateUserDTO) -> User:
        return User(
            
            external_id=dto.external_id,
            messenger_type=dto.messenger_type,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            account_id=dto.account_id,
            created_at = datetime.utcnow()
        )
    
    @classmethod
    def create_to_response_dto(entity: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=entity.id,
            external_id=entity.external_id,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            account_id=entity.account_id,
            created_at=entity.created_at,            
        )
    


# --- app/application/mappers/account_mapper.py ---
from app.application.dto.account_dto import AccountResponseDTO, CreateAccountDTO
from app.domain.entities.account import Account


class AccountMapper:
    @staticmethod
    def create_dto_to_entity(dto: CreateAccountDTO) -> Account:
        return Account(
            
            email=dto.email,
            phone=dto.phone,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )

    @staticmethod
    def create_to_response_dto(entity: Account) -> AccountResponseDTO:
        return AccountResponseDTO(
            id=entity.id,
            email=entity.email,
            phone=entity.phone,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at,
        )
    


# --- app/presentation/web/web_app.py ---
import logging
import os
from app.core.config.settings import Config
from fastapi import FastAPI, Request, Response, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from app.presentation.telegram.main import create_bot

from app.presentation.web.routes.telegram import router as tg_router 
from app.presentation.web.routes.accounts import router as test_router 
from aiogram.types import ChatAdministratorRights


SECRET_TOKEN = "secrettoken"

async def create_app(config: Config) -> FastAPI:
    app = FastAPI(title="Chatty")    

    bot, dp = create_bot(config=config)
    app.state.bot = bot
    app.state.dp = dp

    app.include_router(tg_router)
    app.include_router(test_router)
    
    @app.on_event("startup")
    async def startup():
        '''Операции выпоняемые при запуске'''
        rights = ChatAdministratorRights(
            is_anonymous=False,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=False,
            can_change_info=True,
            can_invite_users=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_pin_messages=True,
            can_manage_topics=True,
            can_post_stories=False,
            can_edit_stories=False,
            can_delete_stories=False,
        )
        await bot.set_webhook(
            url=f"https://userver05.ru/tgbot/",
            drop_pending_updates=True,
            secret_token=SECRET_TOKEN,
        )
        await bot.set_my_default_administrator_rights(rights)
        logging.info("Установлены вебхуки")
        

        
    @app.on_event("shutdown")
    async def shutdown():
        '''Операции выполныемые при остановке'''
        await bot.delete_webhook()
        await bot.session.close()
        logging.info("Удалены вебхуки")

    return app



# --- app/presentation/web/routes/accounts.py ---
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


# --- app/presentation/web/routes/telegram.py ---
from fastapi import APIRouter, Request, Response, HTTPException, Header
from app.core.config.settings import Config
from aiogram.types import Update
from app.presentation.telegram.main import create_bot


router = APIRouter(prefix="/tgbot", tags=["Telegram Updates"], include_in_schema=True)
SECRET_TOKEN = "secrettoken"
config = Config.load()


# Обработчик вебхуков Telegram
@router.post("/", name="Обновления телеграм")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None),
):
    app = request.app
    dp = app.state.dp
    bot = app.state.bot
    # --- Проверка секретного токена ---
    if x_telegram_bot_api_secret_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return Response(status_code=200)




# --- app/presentation/telegram/main.py ---
from aiogram import Bot, Dispatcher
from app.core.config.loader import load_modules
from app.core.config.settings import Config
from app.presentation.telegram.handlers.base import router



def create_bot(config: Config):
    bot = Bot(token=config.telegram.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    load_modules(dp=dp)
    return bot, dp





# --- app/presentation/telegram/handlers/base.py ---
from aiogram import Router, types
from aiogram.filters import Command

from app.application.di.container import Container
from app.application.dto.user_dto import CreateUserDTO
from app.application.dto.account_dto import CreateAccountDTO
from app.domain.enums.messenger_type import MessengerType

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start - регистрация пользователя"""
    container = Container()
    account_service = container.account_service()
    user_service = container.user_service()
    
    try:
        # Сначала пытаемся найти существующего пользователя
        existing_user = await user_service.get_user_by_external_id(
            external_id=str(message.from_user.id),
            messenger_type=MessengerType.TELEGRAM
        )
        
        if existing_user:
            # Пользователь существует, получаем аккаунт
            account = await account_service.get_account(existing_user.account_id)
            await message.answer(
                f"С возвращением, {account.username or account.first_name}!\n"
                f"Ваш аккаунт: {account.id}\n"
                f"Пользователь: {existing_user.id}"
            )
        else:
            # Создаем DTO для пользователя (account_id будет установлен позже)
            user_dto = CreateUserDTO(
                external_id=str(message.from_user.id),
                messenger_type=MessengerType.TELEGRAM,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                account_id=0  # ✅ Временное значение, будет заменено в create_account_with_user
            )
            
            # Создаем DTO для аккаунта
            account_dto = CreateAccountDTO(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            
            # Создаем аккаунт и пользователя
            account_dto, user_dto = await account_service.create_account_with_user(
                account_dto=account_dto,
                user_dto=user_dto
            )
            
            await message.answer(
                f"Добро пожаловать, {account_dto.username or account_dto.first_name}!\n"
                f"Ваш аккаунт: {account_dto.id}\n"
                f"Пользователь: {user_dto.id}"
            )
        
    except Exception as e:
        await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
        print(f"Error in cmd_start: {e}")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Показать профиль пользователя"""
    container = Container()
    account_service = container.account_service()
    user_service = container.user_service()
    
    try:
        # Ищем пользователя через user_service
        user = await user_service.get_user_by_external_id(
            external_id=str(message.from_user.id),
            messenger_type=MessengerType.TELEGRAM
        )
        
        if user:
            account = await account_service.get_account(user.account_id)
            users = await user_service.get_users_by_account_id(account.id)
            
            await message.answer(
                f"Ваш профиль:\n"
                f"Аккаунт: {account.username or 'Не указан'}\n"
                f"Имя: {account.first_name or 'Не указано'}\n"
                f"Фамилия: {account.last_name or 'Не указана'}\n"
                f"Пользователей в аккаунте: {len(users)}"
            )
        else:
            await message.answer("Профиль не найден. Используйте /start для регистрации.")
            
    except Exception as e:
        await message.answer("Произошла ошибка при получении профиля.")
        print(f"Error in cmd_profile: {e}")


# --- app/presentation/telegram/mappers/user_mapper.py ---
from aiogram.types import User
from app.domain.enums.messenger_type import MessengerType
from app.application.dto.account_dto import CreateAccountDTO
from app.application.dto.user_dto import CreateUserDTO


class TelegramUserMapper:

    @staticmethod
    def to_create_account_dto(telegram_user: User) -> CreateAccountDTO:
        return CreateAccountDTO(
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
        )
    
    @staticmethod
    def to_create_user_dto(telegram_user: User, account_id: int) -> CreateUserDTO:
        return CreateUserDTO(
            external_id=str(telegram_user.id),
            messenger_type=MessengerType.TELEGRAM,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            account_id=account_id
        )
    


# --- app/modules/antispam/handlers.py ---
from aiogram import Router, types
from .service import AntispamService

router = Router()

@router.message()
async def check_spam(message: types.Message):
    service = AntispamService()
    result = await service.check_message(message.text)

    if result.is_spam:
        await message.delete()
        await message.answer(f"🚫 Обнаружен спам ({result.rule})", reply=False)



# --- app/modules/antispam/service.py ---
from dataclasses import dataclass
from . import rules

# Храним последние сообщения пользователей (можно вынести в Redis)
_user_messages: dict[int, list[str]] = {}


@dataclass
class CheckResult:
    is_spam: bool
    rule: str | None = None


class AntispamService:
    async def check_message(self, text: str, user_id: int = 0) -> CheckResult:
        if not text:
            return CheckResult(False)

        # Правило 1: ссылки
        if rules.contains_links(text):
            return CheckResult(True, "links")

        # Правило 2: флуд (слишком часто)
        if rules.is_flood(user_id):
            return CheckResult(True, "flood")

        # Правило 3: повторяющийся текст
        history = _user_messages.get(user_id, [])
        if rules.is_repeated_text(text, history):
            return CheckResult(True, "repeated")

        # Если всё чисто — запоминаем сообщение
        _user_messages.setdefault(user_id, []).append(text)
        if len(_user_messages[user_id]) > 10:
            _user_messages[user_id] = _user_messages[user_id][-10:]  # храним последние 10

        return CheckResult(False)



# --- app/modules/antispam/rules.py ---
import re
from datetime import datetime, timedelta

# Временное хранилище для флуда (можно потом заменить на Redis)
_user_last_msg_time: dict[int, datetime] = {}


def contains_links(text: str) -> bool:
    """
    Проверяет наличие ссылок в сообщении.
    """
    if not text:
        return False
    link_pattern = re.compile(r"(https?://|t\.me/|@[\w_]+)")
    return bool(link_pattern.search(text))


def is_flood(user_id: int, now: datetime | None = None) -> bool:
    """
    Проверяет, отправляет ли пользователь слишком часто.
    """
    now = now or datetime.utcnow()
    last_time = _user_last_msg_time.get(user_id)

    _user_last_msg_time[user_id] = now

    if last_time and now - last_time < timedelta(seconds=2):
        return True
    return False


def is_repeated_text(text: str, history: list[str]) -> bool:
    """
    Проверяет повторяющиеся сообщения (дубликаты).
    """
    text = text.strip().lower()
    if not text or len(history) < 1:
        return False

    duplicates = sum(1 for msg in history if msg.lower() == text)
    return duplicates > 2



# --- app/modules/antispam/__init__.py ---



# --- app/core/config/logging.py ---
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

class ColorFormatter(logging.Formatter):
    """Форматтер с цветами ТОЛЬКО для консоли."""

    COLORS = {
        logging.DEBUG: "\033[34m",   # Синий
        logging.INFO: "\033[32m",    # Зелёный
        logging.WARNING: "\033[33m", # Жёлтый
        logging.ERROR: "\033[31m",   # Красный
        logging.CRITICAL: "\033[41m" # Белый текст на красном фоне
    }
    RESET = "\033[0m"

    def format(self, record):
        # Сохраняем оригинальный уровень для файла
        original_levelname = record.levelname
        
        # Добавляем цвет только для консоли
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        
        result = super().format(record)
        
        # Восстанавливаем оригинальный уровень для других форматтеров
        record.levelname = original_levelname
        return result


def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    log_file: str = "app.log",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """
    Настройка логирования с цветами в консоли и чистым файлом.
    """

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file

    # --- Форматтеры ---
    base_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # РАЗНЫЕ форматтеры для консоли и файла
    console_formatter = ColorFormatter(fmt=base_format, datefmt=date_format)
    file_formatter = logging.Formatter(fmt=base_format, datefmt=date_format)  # БЕЗ цветов

    # --- Хендлеры ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)  # Используем форматтер БЕЗ цветов

    # --- Root logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # --- Настройка uvicorn логгеров ---
    uvicorn_loggers = ["uvicorn", "uvicorn.access", "uvicorn.error"]
    
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(level)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True  # Используем хендлеры root логгера

    # --- Настройка других логгеров ---
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.INFO)

    return root_logger


# --- app/core/config/loader.py ---
import logging
import importlib
import pkgutil
from aiogram import Dispatcher

def load_modules(dp: Dispatcher):
    import app.modules as modules_pkg
    
    loaded_modules = []
    
    for _, module_name, _ in pkgutil.iter_modules(modules_pkg.__path__):
        try:
            mod = importlib.import_module(f"app.modules.{module_name}.handlers")
            if hasattr(mod, "router"):
                dp.include_router(mod.router)
                loaded_modules.append(module_name)
                logging.debug(f"✅ Модуль загружен: {module_name}")
            else:
                logging.warning(f"⚠️ В модуле {module_name} нет router")
        except Exception as e:
            logging.error(f"❌ Ошибка загрузки модуля {module_name}: {e}")
    
    logging.debug(f"📦 Всего загружено модулей: {len(loaded_modules)}: {loaded_modules}")



# --- app/core/config/settings.py ---
from functools import lru_cache
from typing import Literal
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigBase(BaseSettings):
    """Базовый класс для всех конфигов."""
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



class EnvironmentConfig(ConfigBase):
    """Определяет текущее окружение приложения."""
    model_config = SettingsConfigDict(env_prefix="APP_")

    env: Literal["dev", "prod", "test"] = "dev"
    debug: bool = True



class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="TG_",
        env_file=".env",
    )

    bot_token: str
    bot_id: int


class RedisConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
    )

    host: str = "localhost"
    port: int = 6379
    db: int = 0


class DBConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
    )

    url: str
    pool_size: int = 10

class WebConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="WEB_",
        env_file=".env"
    )
    host: str = "localhost"
    port: int = 1255


# === ГЛАВНАЯ КОНФИГУРАЦИЯ ===

class Config(BaseModel):
    """Объединённая конфигурация проекта."""
    env: EnvironmentConfig
    telegram: TelegramConfig
    db: DBConfig
    redis: RedisConfig
    web: WebConfig

    @classmethod
    @lru_cache
    def load(cls) -> "Config":
        """
        Загружает все конфиги из соответствующего .env-файла и кэширует результат.
        Выбирает .env автоматически по окружению (например: .env.prod, .env.dev).
        """
        env_cfg = EnvironmentConfig()
        if env_cfg.env == "dev":
            env_file = ".env.dev"
        else:
            env_file = f".env.{env_cfg.env}"
        telegram = TelegramConfig(_env_file=env_file)
        db = DBConfig(_env_file=env_file)
        redis = RedisConfig(_env_file=env_file)
        web = WebConfig(_env_file=env_file)

        return cls(env=env_cfg, telegram=telegram, db=db, redis=redis, web=web)



# --- app/infrastructure/db/session.py ---
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config.settings import Config



config = Config.load()

engine = create_async_engine(
    url=config.db.url,
    future=True,
    echo=False
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# --- app/infrastructure/db/uow.py ---
from typing import Any, Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories import AccountRepositoryImpl, UserRepositoryImpl
from app.infrastructure.db.session import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repositories: Dict[str, Any] = {}

    async def commit(self):
        '''Коммит транзакции'''
        if self.session:
            await self.session.commit()
    async def rollback(self):
        '''Откат транзакции'''
        if self.session:
            await self.session.rollback()

    async def close(self):
        '''Закрытые транзакции'''
        if self.session:
            await self.session.close()
            self.session = None
            self._repositories.clear()

    async def __aenter__(self):
        self.session = self._session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if not self.session:
            return
        
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            await self.rollback
            raise e
        finally:
            await self.session.close()

    # --- Internal ---
    def _require_session(self) -> AsyncSession:
        if not self.session:
            raise RuntimeError("UoW не инициализирован. Используй 'async with uow'")
        return self.session
    
    def _get_ropositories(self, repo_class: Type, key: str):
        '''Получение репозитория с кешированием'''

        if key not in self._repositories:
            self._repositories[key] = repo_class(self._require_session())
        return self._repositories[key]
    
    # --- Repositories ---
    @property
    def account(self) -> AccountRepositoryImpl:
        return self._get_ropositories(AccountRepositoryImpl, "account")

    @property
    def user(self) -> UserRepositoryImpl:
        return self._get_ropositories(UserRepositoryImpl, "user")




# --- app/infrastructure/db/__init__.py ---



# --- app/infrastructure/db/models/user_model.py ---
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.enums.messenger_type import MessengerType
from app.infrastructure.db.models import BaseModel


if TYPE_CHECKING:
    from app.infrastructure.db.models import AccountModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(String)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    messenger_type: Mapped[MessengerType] =  mapped_column(Enum(MessengerType))
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["AccountModel"]= relationship("AccountModel", back_populates="users")



# --- app/infrastructure/db/models/account_model.py ---
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models import BaseModel


if TYPE_CHECKING:
    from app.infrastructure.db.models import UserModel


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)

    users: Mapped[List["UserModel"]] = relationship("UserModel", back_populates="account")



# --- app/infrastructure/db/models/base_model.py ---
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


# --- app/infrastructure/db/models/__init__.py ---
from .base_model import BaseModel
from .account_model import AccountModel
from .user_model import UserModel


__all__ = (
    "BaseModel",
    "AccountModel",
    "UserModel",
)


# --- app/infrastructure/db/repositories/user_repository_impl.py ---
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_mapper import UserDbMapper
from .base import BaseRepositoryImpl

class UserRepositoryImpl(BaseRepositoryImpl[User, UserModel], UserRepository):
    """Реализация репозитория пользователей с типизированным маппером"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model_class=UserModel,
            mapper=UserDbMapper()  # ✅ Типизированный маппер User ↔ UserModel
        )
    
    async def get_by_external_id(self, external_id: str, messenger_type: str) -> Optional[User]:
        """Поиск пользователя по external_id и messenger_type"""
        stmt = select(self.model_class).where(
            self.model_class.external_id == external_id,
            self.model_class.messenger_type == messenger_type
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_by_account_id(self, account_id: int) -> List[User]:
        """Получение всех пользователей аккаунта"""
        stmt = select(self.model_class).where(self.model_class.account_id == account_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_messenger_type(self, messenger_type: str) -> List[User]:
        """Получение пользователей по типу мессенджера"""
        stmt = select(self.model_class).where(self.model_class.messenger_type == messenger_type)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]


# --- app/infrastructure/db/repositories/user_repository.py ---
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.mappers.user_mapper import UserDbMapper
from .base import BaseRepositoryImpl

class UserRepositoryImpl(BaseRepositoryImpl[User, UserModel], UserRepository):
    """Реализация репозитория пользователей с SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model_class=UserModel,
            mapper=UserDbMapper()
        )
    
    async def get_by_external_id(self, external_id: str, messenger_type: str) -> Optional[User]:
        stmt = select(self.model_class).where(
            self.model_class.external_id == external_id,
            self.model_class.messenger_type == messenger_type
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_by_account_id(self, account_id: int) -> List[User]:
        stmt = select(self.model_class).where(self.model_class.account_id == account_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]


# --- app/infrastructure/db/repositories/account_repository.py ---
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.account import Account
from app.domain.repositories.account import AccountRepository
from app.infrastructure.db.models.account_model import AccountModel
from app.infrastructure.db.mappers.account_mapper import AccountDbMapper
from .base import BaseRepositoryImpl

class AccountRepositoryImpl(BaseRepositoryImpl[Account, AccountModel], AccountRepository):
    """Реализация репозитория аккаунтов с SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model_class=AccountModel,
            mapper=AccountDbMapper()
        )
    
    async def get_by_username(self, username: str) -> Optional[Account]:
        stmt = select(self.model_class).where(self.model_class.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_by_email(self, email: str) -> Optional[Account]:
        stmt = select(self.model_class).where(self.model_class.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)


# --- app/infrastructure/db/repositories/account_repository_impl.py ---
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.account import Account
from app.domain.repositories.account import AccountRepository
from app.infrastructure.db.models.account_model import AccountModel
from app.infrastructure.db.mappers.account_mapper import AccountDbMapper
from app.domain.repositories.interfaces import IEntityMapper
from .base import BaseRepositoryImpl

class AccountRepositoryImpl(BaseRepositoryImpl[Account, AccountModel], AccountRepository):
    """Реализация репозитория аккаунтов с типизированным маппером"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            model_class=AccountModel,
            mapper=AccountDbMapper()  # ✅ Теперь тип IEntityMapper[Account, AccountModel]
        )
    
    async def get_by_username(self, username: str) -> Optional[Account]:
        stmt = select(self.model_class).where(self.model_class.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_by_email(self, email: str) -> Optional[Account]:
        stmt = select(self.model_class).where(self.model_class.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)


# --- app/infrastructure/db/repositories/base.py ---
from typing import Generic, TypeVar, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.repositories.base import BaseRepository
from app.domain.repositories.interfaces import IEntityMapper

T = TypeVar('T')  # Domain Entity
M = TypeVar('M')  # SQLAlchemy Model

class BaseRepositoryImpl(BaseRepository[T], Generic[T, M]):
    """Базовая реализация репозитория с типизированным маппером"""
    
    def __init__(
        self, 
        session: AsyncSession, 
        model_class: Type[M], 
        mapper: IEntityMapper[T, M]  # ✅ Теперь с интерфейсом
    ):
        self.session = session
        self.model_class = model_class
        self.mapper = mapper
    
    async def create(self, entity: T) -> T:
        model = self.mapper.to_model(entity)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self.mapper.to_entity(model)
    
    async def get(self, id: int) -> Optional[T]:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_all(self) -> List[T]:
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def update(self, id: int, entity: T) -> Optional[T]:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        update_data = entity.dict(exclude={'id', 'created_at'})
        for field, value in update_data.items():
            if hasattr(model, field) and value is not None:
                setattr(model, field, value)
        
        await self.session.flush()
        await self.session.refresh(model)
        return self.mapper.to_entity(model)
    
    async def delete(self, id: int) -> bool:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True


# --- app/infrastructure/db/repositories/__init__.py ---
from app.infrastructure.db.repositories.account_repository import AccountRepositoryImpl
from app.infrastructure.db.repositories.user_repository import UserRepositoryImpl


__all__ = (
    "AccountRepositoryImpl",
    "UserRepositoryImpl",
)



# --- app/infrastructure/db/mappers/user_mapper.py ---
from typing import Optional
from app.domain.entities.user import User
from app.infrastructure.db.models.user_model import UserModel
from app.domain.repositories.interfaces import IEntityMapper
from app.domain.enums.messenger_type import MessengerType

class UserDbMapper(IEntityMapper[User, UserModel]):
    """Реализация маппера для User Entity ↔ UserModel"""
    
    def to_entity(self, model: UserModel) -> Optional[User]:
        if not model:
            return None
            
        return User(
            id=model.id,
            external_id=model.external_id,
            messenger_type=MessengerType(model.messenger_type),
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            account_id=model.account_id,
            created_at=model.created_at
        )
    
    def to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            external_id=entity.external_id,
            messenger_type=entity.messenger_type.value,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            account_id=entity.account_id,
            created_at=entity.created_at
        )


# --- app/infrastructure/db/mappers/account_mapper.py ---
from typing import Optional
from app.domain.entities.account import Account
from app.infrastructure.db.models.account_model import AccountModel
from app.domain.repositories.interfaces import IEntityMapper

class AccountDbMapper(IEntityMapper[Account, AccountModel]):
    """Реализация маппера для Account Entity ↔ AccountModel"""
    
    def to_entity(self, model: AccountModel) -> Optional[Account]:
        if not model:
            return None
            
        return Account(
            id=model.id,
            email=model.email,
            phone=model.phone,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            created_at=model.created_at
        )
    
    def to_model(self, entity: Account) -> AccountModel:
        return AccountModel(
            id=entity.id,
            email=entity.email,
            phone=entity.phone,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at
        )

