from typing import Any, Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories import AccountRepositoryImpl, UserRepositoryImpl
from app.infrastructure.db.session import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repositories: Dict[str, Any] = {}

    async def commit(self):
        '''Коммит транзакции'''
        if self.session:
            await self.session.commit()
    async def rollback(self):
        '''Откат транзакции'''
        if self.session:
            await self.session.rollback()

    async def close(self):
        '''Закрытые транзакции'''
        if self.session:
            await self.session.close()
            self.session = None
            self._repositories.clear()

    async def __aenter__(self):
        self.session = self._session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        if not self.session:
            return
        
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            await self.rollback()
            raise e
        finally:
            await self.session.close()

    # --- Internal ---
    def _require_session(self) -> AsyncSession:
        if not self.session:
            raise RuntimeError("UoW не инициализирован. Используй 'async with uow'")
        return self.session
    
    def _get_ropositories(self, repo_class: Type, key: str):
        '''Получение репозитория с кешированием'''

        if key not in self._repositories:
            self._repositories[key] = repo_class(self._require_session())
        return self._repositories[key]
    
    # --- Repositories ---
    @property
    def account(self) -> AccountRepositoryImpl:
        return self._get_ropositories(AccountRepositoryImpl, "account")

    @property
    def user(self) -> UserRepositoryImpl:
        return self._get_ropositories(UserRepositoryImpl, "user")

