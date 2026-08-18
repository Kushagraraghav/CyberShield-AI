"""Evidence schemas."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
class EvidenceCreate(BaseModel):
    """Evidence creation schema."""
    case_id: UUID
    organization_id: UUID
    evidence_number: str = Field(..., max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    evidence_type: str = Field(
        ..., pattern="^(disk_image|memory_dump|log|document|network_capture|executable|other)$"
    )
    file_name: str | None = Field(None, max_length=500)
    file_size: int | None = None
    sha256_hash: str | None = Field(None, max_length=64)
    md5_hash: str | None = Field(None, max_length=32)
    storage_path: str | None = Field(None, max_length=1000)
    metadata: dict | None = None
    collected_at: datetime
    collected_by: UUID | None = None
class EvidenceUpdate(BaseModel):
    """Evidence update schema."""
    name: str | None = Field(None, max_length=255)
    description: str | None = Field(None, max_length=2000)
    evidence_type: str | None = Field(
        None, pattern="^(disk_image|memory_dump|log|document|network_capture|executable|other)$"
    )
class EvidenceResponse(BaseModel):
    """Evidence response schema."""
    id: UUID
    case_id: UUID
    organization_id: UUID
    evidence_number: str
    name: str
    description: str | None
    evidence_type: str
    file_name: str | None
    file_size: int | None
    sha256_hash: str | None
    md5_hash: str | None
    storage_path: str | None
    collected_at: datetime
    collected_by: UUID | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class EvidenceDetailResponse(EvidenceResponse):
    """Detailed evidence response schema."""
    pass
