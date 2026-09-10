from datetime import datetime

from pydantic import BaseModel


class RepositoryResponse(BaseModel):
    id: str
    project_id: str
    name: str
    source_type: str
    source_url: str | None
    status: str
    created_at: datetime