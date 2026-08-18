"""Evidence integrity verification schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EvidenceIntegrityVerificationCreate(BaseModel):
    """Create an evidence integrity verification."""

    evidence_id: UUID
    algorithm: str = Field(
        ...,
        pattern="^(sha256|md5)$",
    )
    expected_hash: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )
    calculated_hash: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )
    status: str = Field(
        ...,
        pattern="^(verified|failed)$",
    )
    details: str | None = None
    verified_by: UUID | None = None


class EvidenceIntegrityVerificationResponse(BaseModel):
    """Evidence integrity verification response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: UUID
    algorithm: str
    expected_hash: str
    calculated_hash: str
    status: str
    details: str | None
    verified_at: datetime
    verified_by: UUID | None
