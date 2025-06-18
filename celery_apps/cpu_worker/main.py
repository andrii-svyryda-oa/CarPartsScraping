from celery import Celery
from common.settings import settings

import common.database.models # noqa: F401

celery_app = Celery(
    'cpu_worker', 
    broker=settings.REDIS_BROKER_URL, backend=settings.REDIS_RESULT_BACKEND or settings.REDIS_BROKER_URL
)

celery_app.conf.imports = ["celery_apps.cpu_worker.training.tasks"]
