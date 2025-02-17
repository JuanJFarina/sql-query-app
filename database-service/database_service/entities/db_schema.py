from pydantic import BaseModel
from typing import Any


class DbSchema(BaseModel):
    db_schema: list[dict[str, Any]]
