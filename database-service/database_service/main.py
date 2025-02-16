from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os

app = FastAPI()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_SERVICE = os.environ.get("POSTGRES_SERVICE")

CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVICE}:5432/{POSTGRES_DB}"

print(
    "CONNECTING TO POSTGRESQL DATABASE\n"
    f"User: {POSTGRES_USER}\nService: {POSTGRES_SERVICE}\n"
    f"Database: {POSTGRES_DB}"
)

engine = create_engine(CONNECTION_STRING)


@app.post("/execute_query")
async def execute_query(query: str) -> dict[str, list[dict[str, str]]]:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return {"result": [dict(row) for row in result]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schema")
async def get_schema() -> dict[str, list[dict[str, str]]]:
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT column_name, data_type FROM "
                "information_schema.columns WHERE table_name = 'sales'"
            )
        )
        return {"schema": [dict(row) for row in result]}
