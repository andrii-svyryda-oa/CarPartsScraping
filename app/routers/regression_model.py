from fastapi import APIRouter, status
from app.dependencies.regression_model import RegressionModelCRUDDep, RegressionModelDep
from app.schemas.regression_model import CreateRegressionModelIn, ModelStatsIn, PricePredictionIn, PricePredictionOut, TrainRegressionModelIn, UpdateRegressionModelIn, RegressionModelOut
from common.database.schemas.regression_model import RegressionModelCreate, RegressionModelUpdate
from celery_apps.io_worker.main import celery_app
from common.services.regression.price_regression.metrics import PriceDependencyGraphicsBuilder
from common.services.regression.price_regression.predict import PriceRegressionPredictor

router = APIRouter(prefix="/regression-models", tags=["regression-models"])


@router.get("", response_model=list[RegressionModelOut])
async def get_regression_models(
    regression_model_crud: RegressionModelCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await regression_model_crud.get_multi(skip=skip, limit=limit)


@router.get("/{regression_model_id}", response_model=RegressionModelOut)
async def get_regression_model(regression_model: RegressionModelDep):
    return regression_model


@router.post("", response_model=RegressionModelOut, status_code=status.HTTP_201_CREATED)
async def create_regression_model(
    regression_model_in: CreateRegressionModelIn,
    regression_model_crud: RegressionModelCRUDDep
):
    regression_model_create = RegressionModelCreate(**regression_model_in.model_dump())
    return await regression_model_crud.create(obj_in=regression_model_create)


@router.put("/{regression_model_id}", response_model=RegressionModelOut)
async def update_regression_model(
    regression_model: RegressionModelDep,
    regression_model_in: UpdateRegressionModelIn,
    regression_model_crud: RegressionModelCRUDDep
):
    regression_model_update = RegressionModelUpdate(**regression_model_in.model_dump(exclude_unset=True))
    return await regression_model_crud.update(db_obj=regression_model, obj_in=regression_model_update)


@router.delete("/{regression_model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_regression_model(regression_model: RegressionModelDep, regression_model_crud: RegressionModelCRUDDep):
    await regression_model_crud.remove(id=regression_model.id) 


    
@router.post("/train", status_code=status.HTTP_204_NO_CONTENT)
async def train_regression_model(
    train_regression_model_in: TrainRegressionModelIn
):
    celery_app.send_task("cpu.training.train_price_regression_model", kwargs={
        "category_id": train_regression_model_in.category_id,
        "name": train_regression_model_in.name
    }, queue="cpu_queue")
    

@router.post("/{regression_model_id}/predict", response_model=PricePredictionOut)
async def predict_price(
    predict_price_in: PricePredictionIn,
    regression_model: RegressionModelDep
):
    predictor = PriceRegressionPredictor(regression_model)
    
    prediction = predictor.predict_price(input=predict_price_in)
    
    return prediction

@router.post("/{regression_model_id}/model-stats")
async def get_model_stats(
    model_stats_in: ModelStatsIn,
    regression_model: RegressionModelDep,
):
    graphics_builder = PriceDependencyGraphicsBuilder(
        min_rating=model_stats_in.min_reviews_count,
        max_rating=model_stats_in.max_reviews_count,
        min_search_position=model_stats_in.min_search_position,
        max_search_position=model_stats_in.max_search_position,
        manufacturers=model_stats_in.manufacturers,
        platforms=model_stats_in.platforms,
        regression_model=regression_model
    )
    
    graphics_builder.generate_all_graphics()
    
    return {"graphics_dir": graphics_builder.output_dir}
    
