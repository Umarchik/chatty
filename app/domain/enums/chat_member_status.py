from enum import Enum


class ChatMemberStatus(Enum):
    
    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"

    @classmethod
    def get_by_value(cls, value: str):
        for status in cls:
            if status.value == value:
                return status
        raise ValueError(f"Unknown status: {value}")
