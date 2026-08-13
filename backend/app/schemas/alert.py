"""Alert schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AlertCreate(BaseModel):
    """Alert creation schema."""

    organization_id: UUID
    incident_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    severity: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    status: str = Field(default="new", regex="^(new|acknowledged|investigating|resolved|dismissed)$")
    source: str | None = Field(None, max_length=255)
    source_event_id: str | None = Field(None, max_length=500)
    detected_at: datetime


class AlertUpdate(BaseModel):
    """Alert update schema."""

    title: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=2000)
    severity: str | None = Field(None, regex="^(low|medium|high|critical)$")
    status: str | None = Field(None, regex="^(new|acknowledged|investigating|resolved|dismissed)$")
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None


class AlertResponse(BaseModel):
    """Alert response schema."""

    id: UUID
    organization_id: UUID
    incident_id: UUID | None
    title: str
    description: str | None
    severity: str
    status: str
    source: str | None
    source_event_id: str | None
    detected_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertDetailResponse(AlertResponse):
    """Detailed alert response schema."""

    pass
