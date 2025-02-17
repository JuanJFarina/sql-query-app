import os
import requests
from fastapi import FastAPI, Body, Request
from llmware.models import ModelCatalog
from pydantic import BaseModel

app = FastAPI()

model = ModelCatalog().load_model("slim-sql-tool")

DATABASE_SERVICE = os.environ.get("DATABASE_SERVICE")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_SERVICE_URL = f"http://{DATABASE_SERVICE}:{DATABASE_PORT}"


class UserQuestion(BaseModel):
    question: str


class SQLResponse(BaseModel):
    sql: str


@app.post(
    "/generate_sql",
    response_model=SQLResponse,
)
async def generate_sql(
    request: Request,
    body: UserQuestion = Body(...),
) -> SQLResponse:
    # Fetch schema from Database Service
    schema_response = requests.get(f"{DATABASE_SERVICE_URL}/schema")
    schema = schema_response.json()["db_schema"]
    schema_str = ", ".join(
        [f"{col['column_name']} ({col['data_type']})" for col in schema]
    )

    prompt = f"""
### Task
Generate a SQL query to answer [QUESTION]{body.question}[/QUESTION]

### Database Schema
The query will run on a postgres database table called 'sales' with the following schema:
{schema_str}

### Answer
Return only the corresponding SQL query without any additional text.
"""

    print(f"{prompt = }")

    result = model.inference(prompt)

    return {"sql": result["llm_response"].strip()}
