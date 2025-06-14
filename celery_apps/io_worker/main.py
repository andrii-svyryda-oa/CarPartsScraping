from celery import Celery
from common.settings import settings

celery_app = Celery(
    'io_worker', 
    broker=settings.REDIS_BROKER_URL, backend=settings.REDIS_RESULT_BACKEND or settings.REDIS_BROKER_URL
)

celery_app.conf.imports = ["celery_apps.io_worker.scraping.tasks"]
