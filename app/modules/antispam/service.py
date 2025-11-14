from dataclasses import dataclass
from . import rules

# Храним последние сообщения пользователей (можно вынести в Redis)
_user_messages: dict[int, list[str]] = {}


@dataclass
class CheckResult:
    is_spam: bool
    rule: str | None = None


class AntispamService:
    async def check_message(self, text: str, user_id: int = 0) -> CheckResult:
        if not text:
            return CheckResult(False)

        # Правило 1: ссылки
        if rules.contains_links(text):
            return CheckResult(True, "links")

        # Правило 2: флуд (слишком часто)
        if rules.is_flood(user_id):
            return CheckResult(True, "flood")

        # Правило 3: повторяющийся текст
        history = _user_messages.get(user_id, [])
        if rules.is_repeated_text(text, history):
            return CheckResult(True, "repeated")

        # Если всё чисто — запоминаем сообщение
        _user_messages.setdefault(user_id, []).append(text)
        if len(_user_messages[user_id]) > 10:
            _user_messages[user_id] = _user_messages[user_id][-10:]  # храним последние 10

        return CheckResult(False)
