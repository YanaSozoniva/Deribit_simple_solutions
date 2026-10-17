from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.postgres.price_repo import PriceRepository
from app.postgres.schemas import PriceDTO

router = APIRouter()

@router.get("", response_model=list[PriceDTO])
async def get_all_prices(
    ticker: str = Query(..., description="Тикер валюты (btc_usd и eth_usd)"),
    db: AsyncSession = Depends(get_db),
) -> list[PriceDTO]:
    """Все сохранённые цены по указанной валюте."""
    repo = PriceRepository(db)
    prices = await repo.get_all_by_ticker(ticker)
    return prices

@router.get("/prices/last", response_model=PriceDTO)
async def get_last_price(
    ticker: str = Query(...),
    db: Session = Depends(get_db)
):
    repo = PriceRepository(db)
    price = await repo.get_last_by_ticker(ticker)
    if not price:
        raise HTTPException(status_code=404, detail="Data not found")
    return price

@router.get("/prices/filter", response_model=List[PriceDTO])
async def get_prices_by_date(
    ticker: str = Query(...),
    from_date: int = Query(..., description="UNIX timestamp начала"),
    to_date: int = Query(..., description="UNIX timestamp окончания"),
    db: Session = Depends(get_db)
):
    repo = PriceRepository(db)
    price = await repo.get_by_ticker_and_date_range(ticker, from_date, to_date)
    return price
