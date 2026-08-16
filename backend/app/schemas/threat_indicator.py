"""Threat indicator schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ThreatIndicatorCreate(BaseModel):
    """Threat indicator creation schema."""

    organization_id: UUID
    indicator_type: str = Field(..., pattern="^(ip|domain|url|hash|email)$")
    indicator_value: str = Field(..., min_length=1, max_length=500)
    confidence: int = Field(default=0, ge=0, le=100)
    severity: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    source: str | None = Field(None, max_length=255)
    first_seen: datetime


class ThreatIndicatorUpdate(BaseModel):
    """Threat indicator update schema."""

    confidence: int | None = Field(None, ge=0, le=100)
    severity: str | None = Field(None, pattern="^(low|medium|high|critical)$")
    is_active: bool | None = None
    last_seen: datetime | None = None


class ThreatIndicatorResponse(BaseModel):
    """Threat indicator response schema."""

    id: UUID
    organization_id: UUID
    indicator_type: str
    indicator_value: str
    confidence: int
    severity: str
    source: str | None
    first_seen: datetime
    last_seen: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ThreatIndicatorDetailResponse(ThreatIndicatorResponse):
    """Detailed threat indicator response schema."""

    pass

