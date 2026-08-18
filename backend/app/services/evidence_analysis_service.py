from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence_analysis import EvidenceAnalysis
from app.repositories.evidence_analysis_repository import EvidenceAnalysisRepository


class EvidenceAnalysisService:
    """Business logic for evidence analysis."""

    @staticmethod
    async def create_analysis(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
        analysis_type: str,
        analyzed_by: UUID | None = None,
        tool_used: str | None = None,
        analyst_notes: str | None = None,
    ) -> EvidenceAnalysis:
        analysis = EvidenceAnalysis(
            evidence_id=evidence_id,
            organization_id=organization_id,
            analysis_type=analysis_type,
            status="pending",
            analyzed_by=analyzed_by,
            tool_used=tool_used,
            analyst_notes=analyst_notes,
        )

        return await EvidenceAnalysisRepository.create(db, analysis)

    @staticmethod
    async def get_analysis(
        db: AsyncSession,
        analysis_id: UUID,
        organization_id: UUID,
    ) -> EvidenceAnalysis | None:
        return await EvidenceAnalysisRepository.get_by_id(
            db,
            analysis_id,
            organization_id,
        )

    @staticmethod
    async def list_evidence_analyses(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> Sequence[EvidenceAnalysis]:
        return await EvidenceAnalysisRepository.list_by_evidence(
            db,
            evidence_id,
            organization_id,
        )

    @staticmethod
    async def start_analysis(
        db: AsyncSession,
        analysis: EvidenceAnalysis,
    ) -> EvidenceAnalysis:
        analysis.status = "in_progress"
        analysis.started_at = datetime.now(timezone.utc)

        return await EvidenceAnalysisRepository.update(db, analysis)

    @staticmethod
    async def complete_analysis(
        db: AsyncSession,
        analysis: EvidenceAnalysis,
        findings: str | None = None,
    ) -> EvidenceAnalysis:
        analysis.status = "completed"
        analysis.findings = findings
        analysis.completed_at = datetime.now(timezone.utc)

        return await EvidenceAnalysisRepository.update(db, analysis)

    @staticmethod
    async def fail_analysis(
        db: AsyncSession,
        analysis: EvidenceAnalysis,
        findings: str | None = None,
    ) -> EvidenceAnalysis:
        analysis.status = "failed"
        analysis.findings = findings
        analysis.completed_at = datetime.now(timezone.utc)

        return await EvidenceAnalysisRepository.update(db, analysis)
