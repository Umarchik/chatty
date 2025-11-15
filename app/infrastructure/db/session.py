from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config.settings import Config



config = Config.load()

engine = create_async_engine(
    url=config.db.url,
    future=True,
    echo=False
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)