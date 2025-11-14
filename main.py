import asyncio
import logging
import uvicorn
from app.core.config.logging import setup_logging
from app.core.config.settings import Config
from app.presentation.web.web_app import create_app


async def main():
    config = Config.load()
    log_level = logging.DEBUG if config.env.debug else logging.INFO
    setup_logging(level=log_level)
    logging.info(f"🚀 Приложение запущено в режиме {config.env.env.upper()} (debug={config.env.debug})")

    # создаём FastAPI-приложение (бот + веб)
    app = await create_app(config)
    

    # Настройка uvicorn
    uvicorn_config = uvicorn.Config(
        app=app,
        host=config.web.host,
        port=config.web.port,
        log_level=log_level,
        log_config=None,
        reload=config.env.debug,
        use_colors=False,  
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("❌ Сервер остановлен вручную")
