from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import AccountModel
from app.domain.repositories import IAccountRepository


class AccountRepository(IAccountRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> list[AccountModel]:
        result = await self.session.scalars(select(AccountModel))

    async def get_by_id(self, account_id: int):
        pass

    async def add(self, account: AccountModel):
        pass

    async def delete(self, account_id: int):
        pass


