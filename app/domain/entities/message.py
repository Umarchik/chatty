from typing import TYPE_CHECKING
from pydantic import BaseModel
from datetime import datetime

from ..enums import MessengerType, MessageStatus
from app.domain.entities.chat import Chat
from app.domain.entities.user import User


class Message(BaseModel):
    id: int  
    external_id: str  
    messenger_type: MessengerType
    text: str
    user: User  
    chat: Chat  
    status: MessageStatus
    created_at: datetime
    
    def is_moderated(self) -> bool:
        return self.status != MessageStatus.PENDING
    
    def is_telegram_message(self) -> bool:
        return self.messenger_type == MessengerType.TELEGRAM
    
    def can_be_edited(self) -> bool:
        return self.messenger_type in [MessengerType.TELEGRAM, MessengerType.DISCORD]
    
    def get_messenger_identity(self) -> str:
        """Возвращает идентификатор сообщения в контексте мессенджера"""
        return f"{self.messenger_type}:{self.external_id}"