from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.enums.messenger_type import MessengerType


class CreateUserDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str]  = None
    account: Account

class UpdateUserDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account: Account

class UserResponseDTO(BaseModel):
    id: int
    external_id: str
    username: Optional[str] = None
    first_name: Optional[str]= None
    last_name: Optional[str] = None
    account: Account
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserResponseDTO":
        return cls(
            id = user.id,
            external_id = user.external_id,
            messenger_type = user.messenger_type,
            username = user.username,
            first_name = user.first_name,
            last_name = user.last_name,
            account = user.account,
            created_at = user.created_at
        )

