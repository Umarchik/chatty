from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    VOICE = "voice"
    DOCUMENT = "document"
    STICKER = "sticker"
    LOCATION = "location"
    CONTACT = "contact"
    POLL = "poll"
    ANIMATION = "animation"
    
    @classmethod
    def get_by_value(cls, value: str):
        for msg_type in cls:
            if msg_type.value == value:
                return msg_type
        return cls.TEXT