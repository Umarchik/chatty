from typing import Optional
from app.domain.entities.account import Account
from app.infrastructure.db.models.account_model import AccountModel
from app.domain.repositories.interfaces import IEntityMapper

class AccountDbMapper(IEntityMapper[Account, AccountModel]):
    """Реализация маппера для Account Entity ↔ AccountModel"""
    
    def to_entity(self, model: AccountModel) -> Optional[Account]:
        if not model:
            return None
            
        return Account(
            id=model.id,
            email=model.email,
            phone=model.phone,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            created_at=model.created_at
        )
    
    def to_model(self, entity: Account) -> AccountModel:
        return AccountModel(
            id=entity.id,
            email=entity.email,
            phone=entity.phone,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            created_at=entity.created_at
        )