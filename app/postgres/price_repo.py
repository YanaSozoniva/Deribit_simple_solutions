from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.postgres.price import Price


class PriceRepository:
    """Доступ к данным о ценах валют."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, ticker: str, price: float, timestamp: int) -> Price:
        """Создаёт запись о цены валюты."""

        price = Price(
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self._session.add(price)
        await self._session.flush()
        return price

    async def get_all_by_ticker(self, ticker: str) -> list[Price]:
        """Возвращает все записи по заданной валюте."""
        stmt = (
            select(Price)
            .where(Price.ticker == ticker.lower())
            .order_by(desc(Price.timestamp))
        )

        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_last_by_ticker(self, ticker: str) -> Price | None:
        """Последняя запись по тикеру."""
        stmt = (
            select(Price)
            .where(Price.ticker == ticker.lower())
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ticker_and_date_range(
            self,
            ticker: str,
            from_ts: int,
            to_ts: int,
    ) -> list[Price]:
        """Записи по тикеру в диапазоне UNIX-timestamp (включительно)."""
        stmt = (
            select(Price)
            .where(
                Price.ticker == ticker.lower(),
                Price.timestamp >= from_ts,
                Price.timestamp <= to_ts,
            )
            .order_by(desc(Price.timestamp))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
