from celery import shared_task

@shared_task(queue="cpu_queue")
def process_data():
    pass
