import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import PriceNotFoundError, ExchangeError, AppError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует маппинг доменных исключений на HTTP-ответы."""

    @app.exception_handler(PriceNotFoundError)
    async def _price_not_found(
        request: Request,
        exc: PriceNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(ExchangeError)
    async def _exchange_error(
        request: Request,
        exc: ExchangeError,
    ) -> JSONResponse:
        logger.warning("Exchange error: %s", exc.message)
        return JSONResponse(status_code=502, content={"detail": exc.message})

    @app.exception_handler(AppError)
    async def _app_error(
        request: Request,
        exc: AppError,
    ) -> JSONResponse:
        logger.exception("Unhandled AppError")
        return JSONResponse(status_code=500, content={"detail": exc.message})