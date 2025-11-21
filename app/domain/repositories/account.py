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
    