from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command

from app.presentation.telegram.mappers.user_mapper import TelegramUserMapper


router = Router(name=__name__)

@router.message(Command("start"))
async def start_bot(message: Message):
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Открыть веб-панель", web_app={"url": "https://userver05.ru/tgbot/web"})]
            ]
    )

    account_dto = TelegramUserMapper.to_create_account_dto(message.from_user)
    #print(account_dto)

    user_dto = TelegramUserMapper.to_create_user_dto(message.from_user, account_dto)
    print(user_dto)


    await message.answer(
            f"👋 Привет, {message.from_user.full_name or message.from_user.username}!\n"
            f"Все настройки чатов и модулей доступны через веб-панель ниже:",
            reply_markup=keyboard
    )