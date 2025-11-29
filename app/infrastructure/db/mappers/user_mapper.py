from typing import Optional
from app.domain.entities.user import User
from app.infrastructure.db.models.user_model import UserModel
from app.domain.repositories.interfaces import IEntityMapper
from app.domain.enums.messenger_type import MessengerType

class UserDbMapper(IEntityMapper[User, UserModel]):
    """Реализация маппера для User Entity ↔ UserModel"""
    
    def to_entity(self, model: UserModel) -> Optional[User]:
        if not model:
            return None
            
        return User(
            id=model.id,
            external_id=model.external_id,
            messenger_type=MessengerType(model.messenger_type),
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            account_id=model.account_id,
            created_at=model.created_at
        )
    
    def to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            external_id=entity.external_id,
            messenger_type=entity.messenger_type,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            account_id=entity.account_id,
            created_at=entity.created_at
        )