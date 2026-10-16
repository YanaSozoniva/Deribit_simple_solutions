from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory
from app.deribit_client import DeribitClient


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Отдаёт AsyncSession на время одного запроса."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_deribit_client() -> DeribitClient:
    """Клиент биржи — без состояния, можно создавать на каждый запрос."""
    return DeribitClient()
