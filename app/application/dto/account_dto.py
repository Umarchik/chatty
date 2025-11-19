from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.entities.account import Account


class CreateAccountDTO(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str]  = None

class UpdateAccountDTO(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AccountResponseDTO(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str]= None
    last_name: Optional[str] = None
    created_at: datetime

    @classmethod
    def from_entity(cls, account: Account) -> "AccountResponseDTO":
        return cls(
            id = account.id,
            email = account.email,
            username = account.username,
            first_name = account.first_name,
            last_name = account.last_name,
            created_at = account.created_at
        )

