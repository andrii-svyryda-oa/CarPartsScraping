from celery import Celery
from celery_apps.base import common_task_options
from common.settings import settings

import common.database.models # noqa: F401

default_queue = "cpu_queue"

celery_app = Celery(
    'cpu_worker', 
    broker=settings.REDIS_BROKER_URL, backend=settings.REDIS_RESULT_BACKEND or settings.REDIS_BROKER_URL
)

task_modules = ["celery_apps.cpu_worker.training.tasks"]

celery_app = Celery(
    "io_worker",
    **common_task_options, 
    task_default_queue=default_queue,
    include=task_modules,
    task_routes={
        f"{module}.*": {"queue": default_queue}
        for module in task_modules
    },
)
