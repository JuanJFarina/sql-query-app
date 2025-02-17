from pydantic import BaseModel
from typing import Any


class QueryResult(BaseModel):
    result: list[dict[str, Any]]
