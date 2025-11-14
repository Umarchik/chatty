from enum import Enum


class MessengerType(str, Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    MAX = "MAX"
    VK = "vk"
