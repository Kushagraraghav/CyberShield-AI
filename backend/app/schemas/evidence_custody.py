"""Evidence chain of custody schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EvidenceCustodyCreate(BaseModel):
    """Create a chain of custody event."""

    evidence_id: UUID
    organization_id: UUID
    action: str = Field(
        ...,
        pattern="^(collected|transferred|accessed|analyzed|returned|disposed)$",
    )
    from_holder: str | None = Field(None, max_length=255)
    to_holder: str | None = Field(None, max_length=255)
    location: str | None = Field(None, max_length=500)
    notes: str | None = None
    integrity_hash: str | None = Field(None, max_length=64)
    timestamp: datetime


class EvidenceCustodyResponse(BaseModel):
    """Chain of custody response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: UUID
    organization_id: UUID
    action: str
    performed_by: UUID | None
    from_holder: str | None
    to_holder: str | None
    location: str | None
    notes: str | None
    integrity_hash: str | None
    timestamp: datetime
    created_at: datetime
