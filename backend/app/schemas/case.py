"""Case schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class CaseCreate(BaseModel):
    """Case creation schema."""

    organization_id: UUID
    case_number: str = Field(..., max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    status: str = Field(default="open", regex="^(open|investigating|closed|archived)$")
    priority: str = Field(default="medium", regex="^(low|medium|high|critical)$")


class CaseUpdate(BaseModel):
    """Case update schema."""

    title: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=2000)
    status: str | None = Field(None, regex="^(open|investigating|closed|archived)$")
    priority: str | None = Field(None, regex="^(low|medium|high|critical)$")


class CaseResponse(BaseModel):
    """Case response schema."""

    id: UUID
    organization_id: UUID
    case_number: str
    title: str
    description: str | None
    status: str
    priority: str
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseDetailResponse(CaseResponse):
    """Detailed case response schema."""

    pass
