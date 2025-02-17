from fastapi import FastAPI
from database_service.routes import execute_query_router, get_schema_router
from database_service.utils import seed_data

app = FastAPI(title="Database Service")

app.include_router(execute_query_router)
app.include_router(get_schema_router)

seed_data()
