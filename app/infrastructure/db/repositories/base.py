from typing import Generic, TypeVar, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.repositories.base import BaseRepository
from app.domain.repositories.interfaces import IEntityMapper

T = TypeVar('T')  # Domain Entity
M = TypeVar('M')  # SQLAlchemy Model

class BaseRepositoryImpl(BaseRepository[T], Generic[T, M]):
    """Базовая реализация репозитория с типизированным маппером"""
    
    def __init__(
        self, 
        session: AsyncSession, 
        model_class: Type[M], 
        mapper: IEntityMapper[T, M]  # ✅ Теперь с интерфейсом
    ):
        self.session = session
        self.model_class = model_class
        self.mapper = mapper
    
    async def create(self, entity: T) -> T:
        model = self.mapper.to_model(entity)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self.mapper.to_entity(model)
    
    async def get(self, id: int) -> Optional[T]:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model)
    
    async def get_all(self) -> List[T]:
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def update(self, id: int, entity: T) -> Optional[T]:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        update_data = entity.dict(exclude={'id', 'created_at'})
        for field, value in update_data.items():
            if hasattr(model, field) and value is not None:
                setattr(model, field, value)
        
        await self.session.flush()
        await self.session.refresh(model)
        return self.mapper.to_entity(model)
    
    async def delete(self, id: int) -> bool:
        stmt = select(self.model_class).where(self.model_class.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True