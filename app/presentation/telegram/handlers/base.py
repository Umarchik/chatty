from aiogram import Router, types
from aiogram.filters import Command

from app.application.di.container import Container
from app.application.dto.user_dto import CreateUserDTO
from app.application.dto.account_dto import CreateAccountDTO
from app.domain.enums.messenger_type import MessengerType
from app.presentation.telegram.mappers.user_mapper import TelegramUserMapper

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start - регистрация пользователя"""
    container = Container()
    account_service = container.account_service()
    user_service = container.user_service()
    
    try:
        # Сначала пытаемся найти существующего пользователя
        existing_user = await user_service.get_user_by_external_id(
            external_id=str(message.from_user.id),
            messenger_type=MessengerType.TELEGRAM
        )
        
        if existing_user:
            # Пользователь существует, получаем аккаунт
            account = await account_service.get_account(existing_user.account_id)
            await message.answer(
                f"С возвращением, {account.username or account.first_name}!\n"
                f"Ваш аккаунт: {account.id}\n"
                f"Пользователь: {existing_user.id}"
            )
        else:
            # Создаем DTO для пользователя (account_id будет установлен позже)
            user_dto = TelegramUserMapper.to_create_user_dto(telegram_user=message.from_user)
            
            
            # Создаем DTO для аккаунта
            account_dto = TelegramUserMapper.to_create_account_dto(telegram_user=message.from_user)
            
            # Создаем аккаунт и пользователя
            account_dto, user_dto = await account_service.create_account_with_user(
                account_dto=account_dto,
                user_dto=user_dto
            )
            
            await message.answer(
                f"Добро пожаловать, {account_dto.username or account_dto.first_name}!\n"
                f"Ваш аккаунт: {account_dto.id}\n"
                f"Пользователь: {user_dto.id}"
            )
        
    except Exception as e:
        await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
        print(f"Error in cmd_start: {e}")

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Показать профиль пользователя"""
    container = Container()
    account_service = container.account_service()
    user_service = container.user_service()
    
    try:
        # Ищем пользователя через user_service
        user = await user_service.get_user_by_external_id(
            external_id=str(message.from_user.id),
            messenger_type=MessengerType.TELEGRAM
        )
        
        if user:
            account = await account_service.get_account(user.account_id)
            users = await user_service.get_users_by_account_id(account.id)
            
            await message.answer(
                f"Ваш профиль:\n"
                f"Аккаунт: {account.username or 'Не указан'}\n"
                f"Имя: {account.first_name or 'Не указано'}\n"
                f"Фамилия: {account.last_name or 'Не указана'}\n"
                f"Пользователей в аккаунте: {len(users)}"
            )
        else:
            await message.answer("Профиль не найден. Используйте /start для регистрации.")
            
    except Exception as e:
        await message.answer("Произошла ошибка при получении профиля.")
        print(f"Error in cmd_profile: {e}")