"""Organization member schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class OrganizationMemberCreate(BaseModel):
    """Organization member creation schema."""

    user_id: UUID
    organization_id: UUID
    role: str = Field(default="analyst", pattern="^(admin|analyst|investigator|viewer)$")


class OrganizationMemberUpdate(BaseModel):
    """Organization member update schema."""

    role: str = Field(..., pattern="^(admin|analyst|investigator|viewer)$")


class OrganizationMemberResponse(BaseModel):
    """Organization member response schema."""

    id: UUID
    user_id: UUID
    organization_id: UUID
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

