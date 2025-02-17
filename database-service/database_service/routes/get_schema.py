from fastapi import APIRouter
from sqlalchemy import text
from database_service.entities import DbSchema
from database_service.utils import engine

get_schema_router = APIRouter()


@get_schema_router.get(
    "/schema",
    response_model=DbSchema,
)
async def get_schema() -> DbSchema:
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT column_name, data_type FROM "
                "information_schema.columns WHERE table_name = 'sales'"
            )
        )
        return {
            "db_schema": [
                {"column_name": row.column_name, "data_type": row.data_type}
                for row in result
            ]
        }
