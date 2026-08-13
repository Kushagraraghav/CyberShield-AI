"""Audit log schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AuditLogCreate(BaseModel):
    """Audit log creation schema (internal use only)."""

    organization_id: UUID | None = None
    user_id: UUID | None = None
    action: str = Field(..., max_length=50)
    resource_type: str = Field(..., max_length=100)
    resource_id: str | None = Field(None, max_length=255)
    ip_address: str | None = Field(None, max_length=45)
    user_agent: str | None = Field(None, max_length=500)
    details: str | None = None


class AuditLogResponse(BaseModel):
    """Audit log response schema (read-only)."""

    id: UUID
    organization_id: UUID | None
    user_id: UUID | None
    action: str
    resource_type: str
    resource_id: str | None
    ip_address: str | None
    user_agent: str | None
    details: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
