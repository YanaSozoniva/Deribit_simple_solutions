from decimal import Decimal

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.db.basemodel import BaseORM


class Price(BaseORM):
    """Модель для таблицы price."""
    __tablename__ = 'price'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment='Номер операции')
    ticker: Mapped[str] = mapped_column(comment='Тикер валюты')
    price: Mapped[Decimal] = mapped_column(comment='Текущая цена')
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)
