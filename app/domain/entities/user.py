from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.entities.account import Account
from ..enums.messenger_type import MessengerType


class User(BaseModel):
    id: Optional[int] = None
    external_id: str
    messenger_type: MessengerType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account_id: int
    created_at: Optional[datetime] = None
    
    def get_full_name(self) -> str:
        names = [self.first_name, self.last_name]
        return " ".join([name for name in names if name])
