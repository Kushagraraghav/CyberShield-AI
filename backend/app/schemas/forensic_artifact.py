from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ForensicArtifactBase(BaseModel):
    artifact_type: str
    name: str
    path: str | None = None
    description: str | None = None
    source: str | None = None
    hash_value: str | None = None
    status: str | None = None
    discovered_at: datetime | None = None


class ForensicArtifactCreate(ForensicArtifactBase):
    evidence_id: UUID


class ForensicArtifactUpdate(BaseModel):
    artifact_type: str | None = None
    name: str | None = None
    path: str | None = None
    description: str | None = None
    source: str | None = None
    hash_value: str | None = None
    status: str | None = None
    discovered_at: datetime | None = None


class ForensicArtifactOut(ForensicArtifactBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
