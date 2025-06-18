# Car Parts Scraping in Exists and RIA

## Database Models:

• **CarBrand** (id, name (e.g., "BMW", "Mercedes"), country_origin, created_at, ...)

• **CarModel** (id, brand_id (FK to CarBrand), name (e.g., "X5", "C-Class"), year_from, year_to, body_type, created_at, ...)

• **Platform** (id, name (e.g., "RIA", "Exist"), base_url, search_url_template, is_active, created_at, updated_at, ...)

• **CarModelPlatform** (id, car_model_id (FK to CarModel), platform_id (FK to Platform), platform_url, created_at, ...) - links car models to platforms

• **PartCategory** (id, name (e.g., "Engine", "Brakes"), possible_names, description, created_at, ...)

• **PartManufacturer** (id, name, description, created_at, ...)

• **Part** (id, oem_number (unique, indexed), name, category_id (FK to PartCategory), manufacturer_id (FK to PartManufacturer), specifications, description, created_at, ...) - core parts information

• **part_model_association** (car_model_id (FK to CarModel), part_id (FK to Part)) - many-to-many relationship table

• **ScrapedPartData** (id, part_id (FK to Part), platform_id (FK to Platform), url, title_on_platform, article_number, price, availability_status, delivery_days, seller_name, seller_rating, seller_type, location, warranty_months, reviews_count, search_position, images, scraped_at, ...) - stores scraped data from platforms

• **RegressionModel** (id, name (e.g., "Price Prediction Model"), target_variable (e.g., "price"), feature_variables, coefficients, intercept, r_squared, mean_squared_error, category_id (FK to PartCategory), last_trained_at, training_data_count, preprocessing_params, validation_metrics, feature_importance, ...) - ML models for predictions

## Functions:
• Trigger scraping, for one or multiple categories/platforms

• Train regression model for price per category, based on [platform, search_position, reviews_count]

• Predict price based on parameters via API

• Create metrics for specific regression model, with flexible setup

• API CRUDs for all db models

• Celery: scraping runs on background on dedicated worker, celery beat schedules a task each night to scrape for all cars, celery flower helps tracking tasks

## Development things:
• Resolving route params as dependency

• Run everything in WSL - otherwise problems in celery + async

• Adjusted celery in a way, to allow running async functions + sqlalchemy workaraund to work in celery with asyncpg

• Created launch.json and tasks.json, to easily run all services with debugging