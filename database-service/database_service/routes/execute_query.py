from fastapi import APIRouter, Body, Request, HTTPException
from sqlalchemy import text
from database_service.entities import Query, QueryResult
from database_service.utils import engine

execute_query_router = APIRouter()


@execute_query_router.post(
    "/execute_query",
    response_model=QueryResult,
)
async def execute_query(
    request: Request,
    body: Query = Body(...),
) -> QueryResult:
    with engine.connect() as conn:
        result = conn.execute(text(body.query))
        return {"result": [{"row": str(row)} for row in result]}
