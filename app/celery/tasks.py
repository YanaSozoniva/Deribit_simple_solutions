import asyncio
import time

from app.celery.celery_app import celery_app
from app.db.session import async_session_factory
from app.postgres.models.price import Price
from deribit_client import DeribitClient


@celery_app.task
def fetch_and_save_prices():
    client = DeribitClient()
    tickers = ["btc_usd", "eth_usd"]

    prices = asyncio.run(_fetch_prices_concurrently(client, tickers))

    db = async_session_factory()
    try:
        current_timestamp = int(time.time())
        for ticker, price in prices.items():
            if price is not None:
                record = Price(ticker=ticker, price=price, timestamp=current_timestamp)
                db.add(record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()


async def _fetch_prices_concurrently(client: DeribitClient, tickers: list) -> dict:
    tasks = [client.get_index_price(ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        ticker: (result if not isinstance(result, Exception) else None)
        for ticker, result in zip(tickers, results)
    }