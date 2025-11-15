from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repositories import AccountRepository, UserRepository
from app.infrastructure.db.session import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

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
        finally:
            await self.session.commit()

    # --- Internal ---
    def _require_session(self) -> AsyncSession:
        if not self.session:
            raise RuntimeError("UoW не инициализирован. Используй 'async with uow'")
        return self.session
    
    # --- Repositories ---
    @property
    def account(self) -> AccountRepository:
        return AccountRepository(self._require_session())

    @property
    def user(self) -> UserRepository:
        return UserRepository(self._require_session())

