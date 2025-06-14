from celery import Celery
from common.settings import settings

celery_app = Celery(
    'cpu_worker', 
    broker=settings.REDIS_BROKER_URL, backend=settings.REDIS_RESULT_BACKEND or settings.REDIS_BROKER_URL
)

celery_app.conf.imports = ["celery_apps.cpu_worker.process_data.tasks"]
