from pathlib import Path
import sys

root_path = Path(__file__).parent.parent

sys.path.insert(0, str(root_path))

from common.settings import settings
from celery_apps.io_worker.main import celery_app


concat_and_store_results_task = celery_app.signature(
    "io.scraping.concat_and_store_results",
    kwargs={
        "platform_id2category_id2result_paths": {
            "c812dc22-10da-45df-8de1-f0c8944a62af": {
                "328404b4-7827-49af-8ccd-5fa959a8275a": [
                    settings.FILES_DIR + "/f0245306-ac0a-45c3-919c-20532f987355/c812dc22-10da-45df-8de1-f0c8944a62af/328404b4-7827-49af-8ccd-5fa959a8275a.json"
                ]
            }
        },
        "car_model_id": "06bd5eea-8b2a-468a-a293-64f9be82d99d"
    },
    immutable=True
)

concat_and_store_results_task.apply_async()
