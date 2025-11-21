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