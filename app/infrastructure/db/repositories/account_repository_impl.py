from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.account import Account
from app.domain.repositories.account import AccountRepository
from app.infrastructure.db.models.account_model import AccountModel
from app.infrastructure.db.mappers.account_mapper import AccountDbMapper
from app.infrastructure.db.models.user_model import UserModel
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
    
    async def get_by_user_external_id(self, external_id: str) -> Optional[Account]:
        stmt = (
            select(self.model_class)
            .join(UserModel, AccountModel.id == UserModel.account_id)
            .where(UserModel.external_id==external_id)
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self.mapper.to_entity(model)