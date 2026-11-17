
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

NodeType = Literal[
    "file",
    "function",
    "class",
    "endpoint",
    "resource",
]

RelationshipType = Literal[
    "contains",
    "imports",
    "exposes",
    "handled_by",
    "calls",
    "accesses",
]

class RepositoryInfo(BaseModel):
    repository_id: str
    name: str
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    analyzed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class SourceLocation(BaseModel):
    path: str
    line: int | None = None

class SystemNode(BaseModel):
    id: str
    type: NodeType
    name: str
    role: str | None = None
    source: SourceLocation
    metadata: dict[str, Any] = Field(default_factory=dict)

class RelationshipEvidence(BaseModel):
    file_path: str
    line: int | None = None
    expression: str | None = None

class SystemRelationship(BaseModel):
    id: str
    type: RelationshipType
    source_id: str
    target_id: str
    evidence: RelationshipEvidence

class SystemModelStats(BaseModel):
    file_count: int = 0
    node_count: int = 0
    relationship_count: int = 0

class UnifiedSystemModel(BaseModel):
    schema_version: str = "1.0"

    repository: RepositoryInfo

    nodes: list[SystemNode] = Field(default_factory=list)

    relationships: list[SystemRelationship] = Field(
        default_factory=list
    )

    stats: SystemModelStats = Field(
        default_factory=SystemModelStats
    )