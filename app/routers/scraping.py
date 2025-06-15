from fastapi import APIRouter
from celery_apps.io_worker.main import celery_app

router = APIRouter(prefix="/scraping", tags=["scraping"])

@router.post("/start")
async def start_scraping_end():
    celery_app.send_task("io.scraping.start", queue="io_queue")
