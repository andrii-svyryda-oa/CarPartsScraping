from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.database import DbDep
from common.database.cruds.regression_model import RegressionModelCRUD
from common.database.models.regression_model import RegressionModel
import uuid

def get_regression_model_crud(db: DbDep) -> RegressionModelCRUD:
    return RegressionModelCRUD(db)

RegressionModelCRUDDep = Annotated[RegressionModelCRUD, Depends(get_regression_model_crud)]

async def get_regression_model_by_id(regression_model_id: uuid.UUID, regression_model_crud: RegressionModelCRUDDep) -> RegressionModel:
    regression_model = await regression_model_crud.get(regression_model_id)
    if not regression_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regression model not found"
        )
    return regression_model

RegressionModelDep = Annotated[RegressionModel, Depends(get_regression_model_by_id)] 