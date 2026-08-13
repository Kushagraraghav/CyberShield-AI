"""Incident schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class IncidentCreate(BaseModel):
    """Incident creation schema."""

    case_id: UUID
    organization_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    severity: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    status: str = Field(default="open", regex="^(open|investigating|contained|resolved|closed)$")
    source: str | None = Field(None, max_length=255)
    detected_at: datetime


class IncidentUpdate(BaseModel):
    """Incident update schema."""

    title: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=2000)
    severity: str | None = Field(None, regex="^(low|medium|high|critical)$")
    status: str | None = Field(None, regex="^(open|investigating|contained|resolved|closed)$")
    resolved_at: datetime | None = None


class IncidentResponse(BaseModel):
    """Incident response schema."""

    id: UUID
    case_id: UUID
    organization_id: UUID
    title: str
    description: str | None
    severity: str
    status: str
    source: str | None
    detected_at: datetime
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentDetailResponse(IncidentResponse):
    """Detailed incident response schema."""

    pass
