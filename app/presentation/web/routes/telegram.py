from fastapi import APIRouter, Request, Response, HTTPException, Header
from app.core.config.settings import Config
from aiogram.types import Update
from app.presentation.telegram.main import create_bot


router = APIRouter(prefix="/webhooks", tags=["Telegram Updates"], include_in_schema=True)
SECRET_TOKEN = "secrettoken"
config = Config.load()


# Обработчик вебхуков Telegram
@router.post("/", name="Обновления телеграм")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None),
):
    app = request.app
    dp = app.state.dp
    bot = app.state.bot
    # --- Проверка секретного токена ---
    if x_telegram_bot_api_secret_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return Response(status_code=200)

