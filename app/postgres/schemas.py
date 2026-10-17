from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """Базовый класс для модели"""

    model_config = ConfigDict(from_attributes=True)

class PriceDTO(BaseDTO):
    """Модель для хранения цены"""
    price: float
    ticker: str
    timestamp: int
    id: int
