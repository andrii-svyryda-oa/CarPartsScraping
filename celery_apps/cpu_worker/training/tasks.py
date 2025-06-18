from celery_apps.cpu_worker.main import celery_app
from common.database.cruds.regression_model import RegressionModelCRUD
from common.database.cruds.scraped_part_data import ScrapedPartDataCRUD
from common.services.regression.price_regression.train import PriceRegressionTrainer, PricePredictionTrainingInput
import uuid
from common.database.connection import get_db_celery


@celery_app.task
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
                    seller_name=record.seller_name,
                    location=record.location,
                    platform=record.platform_id,
                    article_number=record.article_number,
                    reviews_count=record.reviews_count,
                    search_position=record.search_position,
                    price=record.price
                )
                for record in scraped_data
            ]
        )
        
        await regression_model_crud.create(obj_in=model)
        
        await db.commit()
        