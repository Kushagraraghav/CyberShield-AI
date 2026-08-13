"""Organization schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class OrganizationCreate(BaseModel):
    """Organization creation schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)


class OrganizationUpdate(BaseModel):
    """Organization update schema."""

    name: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=1000)
    is_active: bool | None = None


class OrganizationResponse(BaseModel):
    """Organization response schema."""

    id: UUID
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationDetailResponse(OrganizationResponse):
    """Detailed organization response schema."""

    pass
