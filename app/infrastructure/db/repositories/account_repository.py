from app.infrastructure.db.models import AccountModel
from app.domain.repositories import IAccountRepository


class AccountRepository(IAccountRepository):
    
    async def get_all(self):
        pass

    async def get_by_id(self, account_id: int):
        pass

    async def add(self, account: AccountModel):
        pass

    async def delete(self, account_id: int):
        pass


