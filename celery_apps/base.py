import asyncio
from common.settings import settings
from celery import Task

class CustomTask(Task):
    def __call__(self, *args, **kwargs):
        # leaving this here to demonstrate that new loop is created for each task
        # try:    
        #     loop = asyncio.get_event_loop()
        #     print(loop)
        # except RuntimeError:
        #     print("No event loop found")

        result = super().__call__(*args, **kwargs)
        
        if asyncio.iscoroutine(result):
            return asyncio.run(result)
        else:
            return result

common_task_options = {
    "broker": settings.REDIS_BROKER_URL, 
    "backend": settings.REDIS_RESULT_BACKEND or settings.REDIS_BROKER_URL,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "task_cls": CustomTask,
}
