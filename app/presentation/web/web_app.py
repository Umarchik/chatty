import logging
import os
from app.core.config.settings import Config
from fastapi import FastAPI, Request, Response, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from app.presentation.telegram.main import create_bot

from app.presentation.web.routes.telegram import router as tg_router 
from app.presentation.web.routes.accounts import router as test_router 
from aiogram.types import ChatAdministratorRights


SECRET_TOKEN = "secrettoken"

async def create_app(config: Config) -> FastAPI:
    app = FastAPI(root_path="/tgbot", title="Chatty")    

    bot, dp = create_bot(config=config)
    app.state.bot = bot
    app.state.dp = dp

    app.include_router(tg_router)
    app.include_router(test_router)
    
    @app.on_event("startup")
    async def startup():
        '''Операции выпоняемые при запуске'''
        rights = ChatAdministratorRights(
            is_anonymous=False,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=False,
            can_change_info=True,
            can_invite_users=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_pin_messages=True,
            can_manage_topics=True,
            can_post_stories=False,
            can_edit_stories=False,
            can_delete_stories=False,
        )
        await bot.set_webhook(
            url=f"https://userver05.ru/tgbot/webhooks/",
            drop_pending_updates=True,
            secret_token=SECRET_TOKEN,
        )
        await bot.set_my_default_administrator_rights(rights)
        logging.info("Установлены вебхуки")
        

        
    @app.on_event("shutdown")
    async def shutdown():
        '''Операции выполныемые при остановке'''
        await bot.delete_webhook()
        await bot.session.close()
        logging.info("Удалены вебхуки")

    return app
