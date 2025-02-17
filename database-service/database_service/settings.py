import os
from pydantic import BaseModel


class _Settings(BaseModel):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVICE: str
    POSTGRES_PORT: str

    @property
    def CONNECTION_STRING(self) -> str:
        print(
            "CONNECTING TO POSTGRESQL DATABASE\n"
            f"User: {self.POSTGRES_USER}\nService: {self.POSTGRES_SERVICE}\n"
            f"Database: {self.POSTGRES_DB}"
        )
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVICE}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


Settings = _Settings(
    POSTGRES_USER=os.environ.get("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
    POSTGRES_DB=os.environ.get("POSTGRES_DB"),
    POSTGRES_SERVICE=os.environ.get("POSTGRES_SERVICE"),
    POSTGRES_PORT=os.environ.get("POSTGRES_PORT"),
)
