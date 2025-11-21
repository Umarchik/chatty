from app.infrastructure.db.uow import UnitOfWork
from app.application.mappers.account_mapper import AccountMapper
from app.application.mappers.user_mapper import UserMapper
from app.application.services.account_service import AccountService
from app.application.services.user_service import UserService

class Container:
    """Контейнер для dependency injection"""
    
    def __init__(self):
        self._uow_class = UnitOfWork
        self._account_mapper = AccountMapper()
        self._user_mapper = UserMapper()
    
    def account_service(self) -> AccountService:
        """Создание сервиса аккаунтов с зависимостями"""
        return AccountService(
            uow_class=self._uow_class,
            account_mapper=self._account_mapper,
            user_mapper=self._user_mapper,
        )
    
    def user_service(self) -> UserService:
        """Создание сервиса пользователей с зависимостями"""
        return UserService(
            uow_class=self._uow_class,
            user_mapper=self._user_mapper,
        )