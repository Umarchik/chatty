from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from redis import int_or_str

from app.domain.entities.account import Account
from app.domain.entities.user import User
from app.domain.enums.messenger_type import MessengerType


class CreateUserDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str]  = None
    account_id: int


class UpdateUserDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    account_id: int_or_str

class UserResponseDTO(BaseModel):
    id: int
    external_id: str
    username: Optional[str] = None
    first_name: Optional[str]= None
    last_name: Optional[str] = None
    account_id: int
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
            account_id = user.account_id,
            created_at = user.created_at
        )

