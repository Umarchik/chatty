from datetime import datetime
from pydantic import BaseModel

from app.domain.entities.chat import Chat
from app.domain.entities.message import Message
from app.domain.entities.user import User
from app.domain.enums.message_status import MessageStatus
from app.domain.enums.messenger_type import MessengerType


class CreateMessageDTO(BaseModel):
    external_id: str
    messenger_type: MessengerType
    text: str
    user: User
    chat: Chat

class UpdateMessageDTO(BaseModel):
    status: MessageStatus

class MessageResponseDTO(BaseModel):
    id: int
    external_id: str
    messenger_type: MessengerType
    text: str
    user: User
    chat: Chat
    status: MessageStatus
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageResponseDTO":
        return cls(
            id = message.id,
            external_id = message.external_id,
            messenger_type = message.messenger_type,
            text = message.text,
            user = message.user,
            chat = message.chat,
            status = message.status,
            created_at = message.created_at
        )