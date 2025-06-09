from src.configs.settings import settings
from src.db.manager import AsyncPGManager

DB_DSN = f"postgresql://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db}"
db_manager = AsyncPGManager(DB_DSN)


async def get_db() -> AsyncPGManager:
    await db_manager.connect()
    try:
        yield db_manager
    finally:
        pass
