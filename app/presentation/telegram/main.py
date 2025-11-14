from aiogram import Bot, Dispatcher
from app.core.config.loader import load_modules
from app.core.config.settings import Config
from app.presentation.telegram.handlers.base import router



def create_bot(config: Config):
    bot = Bot(token=config.telegram.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    load_modules(dp=dp)
    return bot, dp


