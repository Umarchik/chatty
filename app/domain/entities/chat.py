from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..enums import ChatType


class Chat(BaseModel):
    id: int
    external_id: str
    messenger_type: str
    title: Optional[str] = None
    chat_type: ChatType
    created_at: datetime
    
    def is_group_chat(self) -> bool:
        return self.chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]