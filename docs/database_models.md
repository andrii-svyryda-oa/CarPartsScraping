1. Platform (Платформа)

- id: UUID
- name: str
- base_url: str
- search_url_template: str
- is_active: bool
- created_at: datetime
- updated_at: datetime

2. CarBrand (Марка авто)

- id: UUID
- name: str (Toyota, Volkswagen, BMW, etc.)
- country_origin: str
- created_at: datetime

3. CarModel (Модель авто)

- id: UUID
- brand_id: UUID (FK to CarBrand)
- name: str (Camry, Golf, X5, etc.)
- year_from: datetime
- year_to: datetime
- body_type: str (седан, хетчбек, кросовер)
- created_at: datetime

4. PartCategory (Категорія запчастин)

- id: UUID
- name: str (Двигун, Підвіска, Гальмівна система)
- description: str
- created_at: datetime

5. PartManufacturer (Виробник деталі)

- id: UUID
- name: str
- description: str
- created_at: datetime

6. PartModel (Зв'язок запчастини до моделі авто)

- car_model_id: UUID (FK to CarModel)
- part_id: UUID (FK to Part)

7. Part (Запчастина)

- id: UUID
- oem_number: str (оригінальний номер)
- name: str (Фільтр масляний, Колодки гальмівні)
- category_id: UUID (FK to PartCategory)
- manufacturer_id: UUID (FK to PartManufacturer)
- specifications: JSON (розміри, вага, матеріал)
- description: text
- created_at: datetime

8. ScrapedPartData (Зібрані дані)

- id: UUID
- part_id: UUID (FK to Part)
- platform_id: UUID (FK to Platform)
- url: str
- title_on_platform: str
- article_number: str (артикул на платформі)
- price: decimal
- availability_status: str (в наявності, під замовлення)
- delivery_days: int
- seller_name: str
- seller_rating: float
- seller_type: str (магазин, приватна особа)
- location: str (місто)
- warranty_months: int
- reviews_count: int
- search_position: int
- images: JSON (список URL зображень)
- scraped_at: datetime

9. RegressionModel (Модель регресії)

- id: UUID
- name: str (Прогноз ціни на гальмівні колодки)
- target_variable: str (price)
- feature_variables: JSON (["manufacturer", "seller_rating", "delivery_days"])
- coefficients: JSON
- intercept: float
- r_squared: float
- mean_squared_error: float
- category_id: UUID (FK to PartCategory)
- last_trained_at: datetime
- training_data_count: int
