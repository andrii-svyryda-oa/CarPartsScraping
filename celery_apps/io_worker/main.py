from celery import Celery
from celery_apps.base import common_task_options

import common.database.models # noqa: F401

task_modules = ["celery_apps.io_worker.scrape_car_parts.tasks"]

default_queue = "io_queue"

celery_app = Celery(
    "io_worker",
    **common_task_options, # type: ignore
    task_default_queue=default_queue,
    include=task_modules,
    task_routes={
        f"{module}.*": {"queue": default_queue}
        for module in task_modules
    }
)
