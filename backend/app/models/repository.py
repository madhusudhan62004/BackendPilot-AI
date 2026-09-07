from datetime import datetime, timezone

from pydantic import BaseModel, Field


class RepositoryModel(BaseModel):
    name: str
    project_id: str
    source_type: str
    source_url: str | None = None
    status: str = "pending"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )