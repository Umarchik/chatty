from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.enums.messenger_type import MessengerType
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
    
    async def get_by_messenger_type(self, messenger_type: MessengerType) -> List[User]:
        """Получение пользователей по типу мессенджера"""
        stmt = select(self.model_class).where(self.model_class.messenger_type == messenger_type)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]