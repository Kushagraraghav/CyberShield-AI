from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence_analysis import EvidenceAnalysis


class EvidenceAnalysisRepository:
    """Database operations for evidence analysis."""

    @staticmethod
    async def create(
        db: AsyncSession,
        analysis: EvidenceAnalysis,
    ) -> EvidenceAnalysis:
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        return analysis

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        analysis_id: UUID,
        organization_id: UUID,
    ) -> EvidenceAnalysis | None:
        result = await db.execute(
            select(EvidenceAnalysis).where(
                EvidenceAnalysis.id == analysis_id,
                EvidenceAnalysis.organization_id == organization_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_by_evidence(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> Sequence[EvidenceAnalysis]:
        result = await db.execute(
            select(EvidenceAnalysis)
            .where(
                EvidenceAnalysis.evidence_id == evidence_id,
                EvidenceAnalysis.organization_id == organization_id,
            )
            .order_by(EvidenceAnalysis.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        analysis: EvidenceAnalysis,
    ) -> EvidenceAnalysis:
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        return analysis
