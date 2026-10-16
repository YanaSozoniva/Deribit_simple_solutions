from celery import Celery

from app.config import settings

celery_app = Celery(
    "crypto_tracker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.celery.tasks"],
)

celery_app.conf.update(
    beat_schedule={
        "fetch-prices-every-minute": {
            "task": "app.celery.tasks.fetch_and_save_prices",
            "schedule": settings.celery_interval_seconds,
        },
    },
    timezone="UTC",
    enable_utc=True,
    task_ignore_result=True,
    task_track_started=False,
    broker_connection_retry_on_startup=True,
    worker_pool="celery_aio_pool.pool:AsyncIOPool",
)