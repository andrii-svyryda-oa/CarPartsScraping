from celery_apps.cpu_worker.main import celery_app
from common.database.cruds.regression_model import RegressionModelCRUD
from common.database.cruds.scraped_part_data import ScrapedPartDataCRUD
from common.services.regression.price_regression.train import PriceRegressionTrainer, PricePredictionTrainingInput
import uuid
from common.database.connection import get_db_celery


@celery_app.task(name="cpu.training.train_price_regression_model")
async def train_price_regression_model(category_id: uuid.UUID, name: str):
    async with get_db_celery() as db:
        scraped_data_crud = ScrapedPartDataCRUD(db)
        regression_model_crud = RegressionModelCRUD(db)
        
        scraped_data = await scraped_data_crud.get_price_regression_data(category_id)
        
        trainer = PriceRegressionTrainer()
        
        model = trainer.train_regression_model(
            name=name,
            category_id=category_id,
            training_records=[
                PricePredictionTrainingInput(
                    platform=record.platform.name,
                    reviews_count=record.reviews_count or 0,
                    search_position=record.search_position,
                    price=record.price,
                    manufacturer=record.seller_name
                )
                for record in scraped_data
            ]
        )
        
        await regression_model_crud.create(obj_in=model)
        
        await db.commit()
        