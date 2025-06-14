Don't write any comments.
Don't use deprecated typing (Dict, List, Optional).
Use uv as package and venv manager (with pyproject.toml).
This is a FastAPI project, with celery workers.
Use sqlalchemy as ORM with async pg. Use newest version with new syntax. Alembic for db migrations.
For all dependencies specific Annotated variable should be created.
Use pydantic for all schemas.
For database cruds BaseCrud should be created with all basic operations, all other cruds will be inherited from it.
Background tasks separated to 2 groups: cpu intensive, io intensive. Cpu intensive should be executed in cpu_worker, io intensive in io_worker.
