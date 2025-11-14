from enum import Enum


class ChatType(str, Enum):
    PRIVATE = "privite"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
    