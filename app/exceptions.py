class AppError(Exception):
    """Базовое исключение приложения.
    """

    default_message = "Application error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)



class PriceError(AppError):
    """Базовая ошибка при работе с ценами."""


class PriceNotFoundError(PriceError):
    """Цена по тикеру не найдена в БД."""

    def __init__(self, ticker: str) -> None:
        super().__init__(f"Price for ticker '{ticker}' not found")
        self.ticker = ticker


class InvalidTickerError(PriceError):
    """Тикер не поддерживается приложением."""

    def __init__(self, ticker: str) -> None:
        super().__init__(f"Ticker '{ticker}' is not supported")
        self.ticker = ticker


class InvalidDateRangeError(PriceError):
    """Некорректный диапазон дат (from > to)."""

    def __init__(self, from_ts: int, to_ts: int) -> None:
        super().__init__(f"Invalid date range: from={from_ts} > to={to_ts}")
        self.from_ts = from_ts
        self.to_ts = to_ts



class ExchangeError(AppError):
    """Базовая ошибка при обращении к бирже."""


class ExchangeUnavailableError(ExchangeError):
    """Биржа недоступна: сеть, таймаут, 5xx."""

    def __init__(self, detail: str = "") -> None:
        message = "Exchange unavailable"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)
        self.detail = detail


class ExchangeResponseError(ExchangeError):
    """Биржа ответила, но с ошибкой в payload."""

    def __init__(self, detail: str = "") -> None:
        message = "Exchange response error"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)
        self.detail = detail