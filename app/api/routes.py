from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.postgres.price_repo import PriceRepository
from app.postgres.schemas import PriceListDTO, PriceDTO

router = APIRouter()

@router.get("", response_model=list[PriceDTO])
async def get_all_prices(
    ticker: str = Query(..., description="Тикер валюты (BTC, ETH)"),
    db: AsyncSession = Depends(get_db),
) -> list[PriceDTO]:
    """Все сохранённые цены по указанной валюте."""
    repo = PriceRepository(db)
    prices = await repo.get_all_by_ticker(ticker)
    return prices
