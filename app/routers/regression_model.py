from fastapi import APIRouter, status
from app.dependencies.regression_model import RegressionModelCRUDDep, RegressionModelDep
from app.schemas.regression_model import CreateRegressionModelIn, UpdateRegressionModelIn, RegressionModelOut
from common.database.schemas.regression_model import RegressionModelCreate, RegressionModelUpdate

router = APIRouter(prefix="/regression-models", tags=["regression-models"])

@router.get("/", response_model=list[RegressionModelOut])
async def get_regression_models(
    regression_model_crud: RegressionModelCRUDDep,
    skip: int = 0,
    limit: int = 100
):
    return await regression_model_crud.get_multi(skip=skip, limit=limit)

@router.get("/{regression_model_id}", response_model=RegressionModelOut)
async def get_regression_model(regression_model: RegressionModelDep):
    return regression_model

@router.post("/", response_model=RegressionModelOut, status_code=status.HTTP_201_CREATED)
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