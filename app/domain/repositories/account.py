from abc import ABC, abstractmethod
from typing import Sequence
from app.domain.entities.account import Account

class IAccountRepository(ABC):
    @abstractmethod
    async def get_all(self) -> Sequence[Account]:
        pass

    @abstractmethod
    async def get_by_id(self, account_id: int) -> Account | None:
        pass

    @abstractmethod
    async def add(account: Account) -> Account:
        pass

    @abstractmethod
    async def delete(account_id: int):
        pass
