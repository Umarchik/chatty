from app.infrastructure.db.models import UserModel
from app.domain.repositories import IUserRepository


class UserRepository(IUserRepository):
    
    async def get_all(self):
        pass

    async def get_by_id(self, user_id: int):
        pass

    async def add(self, user: UserModel):
        pass

    async def delete(self, user_id: int):
        pass


