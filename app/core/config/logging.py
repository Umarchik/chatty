import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

class ColorFormatter(logging.Formatter):
    """Форматтер с цветами ТОЛЬКО для консоли."""

    COLORS = {
        logging.DEBUG: "\033[34m",   # Синий
        logging.INFO: "\033[32m",    # Зелёный
        logging.WARNING: "\033[33m", # Жёлтый
        logging.ERROR: "\033[31m",   # Красный
        logging.CRITICAL: "\033[41m" # Белый текст на красном фоне
    }
    RESET = "\033[0m"

    def format(self, record):
        # Сохраняем оригинальный уровень для файла
        original_levelname = record.levelname
        
        # Добавляем цвет только для консоли
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        
        result = super().format(record)
        
        # Восстанавливаем оригинальный уровень для других форматтеров
        record.levelname = original_levelname
        return result


def setup_logging(
    level: int = logging.INFO,
    log_dir: str = "logs",
    log_file: str = "app.log",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """
    Настройка логирования с цветами в консоли и чистым файлом.
    """

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file

    # --- Форматтеры ---
    base_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # РАЗНЫЕ форматтеры для консоли и файла
    console_formatter = ColorFormatter(fmt=base_format, datefmt=date_format)
    file_formatter = logging.Formatter(fmt=base_format, datefmt=date_format)  # БЕЗ цветов

    # --- Хендлеры ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)  # Используем форматтер БЕЗ цветов

    # --- Root logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # --- Настройка uvicorn логгеров ---
    uvicorn_loggers = ["uvicorn", "uvicorn.access", "uvicorn.error"]
    
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.setLevel(level)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True  # Используем хендлеры root логгера

    # --- Настройка других логгеров ---
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.INFO)

    return root_logger