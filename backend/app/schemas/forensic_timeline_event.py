from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ForensicTimelineEventBase(BaseModel):
    event_time: datetime
    event_type: str
    title: str
    description: str | None = None
    source: str | None = None
    artifact_id: UUID | None = None
    metadata: dict | None = None


class ForensicTimelineEventCreate(ForensicTimelineEventBase):
    case_id: UUID
    evidence_id: UUID


class ForensicTimelineEventUpdate(BaseModel):
    event_time: datetime | None = None
    event_type: str | None = None
    title: str | None = None
    description: str | None = None
    source: str | None = None
    artifact_id: UUID | None = None
    metadata: dict | None = None


class ForensicTimelineEventOut(ForensicTimelineEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    case_id: UUID
    evidence_id: UUID
    organization_id: UUID
    created_at: datetime
