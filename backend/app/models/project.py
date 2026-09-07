from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    name: str
    description: str | None = None
    owner_id: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )