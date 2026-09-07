from pydantic import BaseModel, Field


class RepositoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    source_type: str
    source_url: str | None = None