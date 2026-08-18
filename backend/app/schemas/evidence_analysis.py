from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EvidenceAnalysisCreate(BaseModel):
    evidence_id: UUID
    organization_id: UUID
    analysis_type: str
    analyzed_by: UUID | None = None
    tool_used: str | None = None
    analyst_notes: str | None = None


class EvidenceAnalysisOut(BaseModel):
    id: UUID
    evidence_id: UUID
    organization_id: UUID
    analysis_type: str
    status: str
    findings: str | None = None
    tool_used: str | None = None
    analyst_notes: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    analyzed_by: UUID | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
