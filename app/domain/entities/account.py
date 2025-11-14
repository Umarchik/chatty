from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class Account(BaseModel):
    """Основной аккаунт пользователя, объединяющий профили из разных мессенджеров"""
    
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    created_at: Optional[datetime] = None
    
    def get_full_name(self) -> str:
        names = [self.first_name, self.last_name]
        return " ".join([name for name in names if name])
