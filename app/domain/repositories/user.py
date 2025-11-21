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
    