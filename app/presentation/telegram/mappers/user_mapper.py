from aiogram.types import User
from app.domain.entities.account import Account
from app.domain.enums.messenger_type import MessengerType
from app.application.dto.account_dto import CreateAccountDTO
from app.application.dto.user_dto import CreateUserDTO


class TelegramUserMapper:

    @staticmethod
    def to_create_account_dto(telegram_user: User) -> CreateAccountDTO:
        return CreateAccountDTO(
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
        )
    
    @staticmethod
    def to_create_user_dto(telegram_user: User, account_id: int) -> CreateUserDTO:
        return CreateUserDTO(
            external_id=str(telegram_user.id),
            messenger_type=MessengerType.TELEGRAM,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            account_id=account_id
        )