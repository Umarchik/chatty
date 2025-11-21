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