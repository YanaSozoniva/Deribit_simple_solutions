import time

from app.celery.celery_app import celery_app
from app.db.session import async_session_factory
from app.postgres.price_repo import PriceRepository
from app.deribit_client import DeribitClient

@celery_app.task(name="app.celery.tasks.fetch_and_save_prices")
async def fetch_and_save_prices() -> None:
    client = DeribitClient()
    async with async_session_factory() as session:
        repo = PriceRepository(session)
        try:
            for ticker in ("btc_usd", "eth_usd"):
                price = await client.get_index_price(ticker)
                await repo.add(
                    ticker=ticker.lower(),
                    price=price,
                    timestamp=int(time.time() * 1000),
                )
            await session.commit()
        except Exception:
            await session.rollback()
            raise
