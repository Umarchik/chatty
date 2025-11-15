from abc import ABC, abstractmethod
from typing import Sequence
from app.domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def get_all(self) -> Sequence[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def add(user: User) -> User:
        pass

    @abstractmethod
    async def delete(user_id: int):
        pass
