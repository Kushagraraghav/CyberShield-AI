"""Threat intelligence feed schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ThreatIntelligenceFeedCreate(BaseModel):
    """Create a threat intelligence feed."""

    organization_id: UUID
    name: str
    feed_type: str
    source: str
    feed_url: str | None = None
    description: str | None = None
    is_active: bool = True


class ThreatIntelligenceFeedUpdate(BaseModel):
    """Update a threat intelligence feed."""

    name: str | None = None
    feed_type: str | None = None
    source: str | None = None
    feed_url: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ThreatIntelligenceFeedResponse(BaseModel):
    """Threat intelligence feed response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    feed_type: str
    source: str
    feed_url: str | None
    description: str | None
    is_active: bool
    last_fetched_at: datetime | None
    last_successful_fetch_at: datetime | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
