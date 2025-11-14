import re
from datetime import datetime, timedelta

# Временное хранилище для флуда (можно потом заменить на Redis)
_user_last_msg_time: dict[int, datetime] = {}


def contains_links(text: str) -> bool:
    """
    Проверяет наличие ссылок в сообщении.
    """
    if not text:
        return False
    link_pattern = re.compile(r"(https?://|t\.me/|@[\w_]+)")
    return bool(link_pattern.search(text))


def is_flood(user_id: int, now: datetime | None = None) -> bool:
    """
    Проверяет, отправляет ли пользователь слишком часто.
    """
    now = now or datetime.utcnow()
    last_time = _user_last_msg_time.get(user_id)

    _user_last_msg_time[user_id] = now

    if last_time and now - last_time < timedelta(seconds=2):
        return True
    return False


def is_repeated_text(text: str, history: list[str]) -> bool:
    """
    Проверяет повторяющиеся сообщения (дубликаты).
    """
    text = text.strip().lower()
    if not text or len(history) < 1:
        return False

    duplicates = sum(1 for msg in history if msg.lower() == text)
    return duplicates > 2
