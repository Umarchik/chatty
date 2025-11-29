from typing import Any
from app.application.di.container import Container


class Depends:
    def __init__(self):
        self._depends = Container()

    def get_accounts_service(self):
        return self._depends.account_service()
    
    def get_users_service(self):
        return self._depends.user_service()
    
depends = Depends()