from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.entities.chat import Chat
from app.domain.enums.chat_type import ChatType
from app.domain.enums.messenger_type import MessengerType


class CreateChatDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    title: Optional[str] = None
    chat_type: ChatType

class UpdateChatDTO(BaseModel):
    title: Optional[str] = None

class ChatResponseDTO(BaseModel):
    id: int
    external_id: str
    messenger_type: MessengerType
    title: Optional[str] = None
    chat_type: ChatType
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatResponseDTO":
        return cls(
            id = chat.id,
            external_id = chat.external_id,
            messenger_type = chat.messenger_type,
            title = chat.title,
            chat_type = chat.chat_type,
            created_at = chat.created_at,
        )