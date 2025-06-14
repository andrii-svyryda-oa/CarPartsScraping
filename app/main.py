from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import common.database.models # noqa: F401
from app.routers import car_brand, car_model, part_category, part_manufacturer, part, platform, regression_model, scraped_part_data

app = FastAPI(
    title="Car Parts API",
    description="API for managing car parts data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Car Parts API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(car_brand.router)
app.include_router(car_model.router)
app.include_router(part_category.router)
app.include_router(part_manufacturer.router)
app.include_router(part.router)
app.include_router(platform.router)
app.include_router(regression_model.router)
app.include_router(scraped_part_data.router)
