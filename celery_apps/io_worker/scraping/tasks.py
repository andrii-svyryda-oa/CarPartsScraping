from celery import shared_task

@shared_task(queue="io_queue")
def scrape_data():
    pass
