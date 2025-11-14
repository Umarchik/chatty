import logging
import importlib
import pkgutil
from aiogram import Dispatcher

def load_modules(dp: Dispatcher):
    import app.modules as modules_pkg
    
    loaded_modules = []
    
    for _, module_name, _ in pkgutil.iter_modules(modules_pkg.__path__):
        try:
            mod = importlib.import_module(f"app.modules.{module_name}.handlers")
            if hasattr(mod, "router"):
                dp.include_router(mod.router)
                loaded_modules.append(module_name)
                logging.debug(f"✅ Модуль загружен: {module_name}")
            else:
                logging.warning(f"⚠️ В модуле {module_name} нет router")
        except Exception as e:
            logging.error(f"❌ Ошибка загрузки модуля {module_name}: {e}")
    
    logging.debug(f"📦 Всего загружено модулей: {len(loaded_modules)}: {loaded_modules}")
