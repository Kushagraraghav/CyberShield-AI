from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forensic_artifact import ForensicArtifact


class ForensicArtifactRepository:
    """Database operations for forensic artifacts."""

    @staticmethod
    async def create(
        db: AsyncSession,
        artifact: ForensicArtifact,
    ) -> ForensicArtifact:
        db.add(artifact)
        await db.flush()
        await db.refresh(artifact)
        return artifact

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        artifact_id: UUID,
        organization_id: UUID,
    ) -> ForensicArtifact | None:
        result = await db.execute(
            select(ForensicArtifact).where(
                ForensicArtifact.id == artifact_id,
                ForensicArtifact.organization_id == organization_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_by_evidence(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> Sequence[ForensicArtifact]:
        result = await db.execute(
            select(ForensicArtifact)
            .where(
                ForensicArtifact.evidence_id == evidence_id,
                ForensicArtifact.organization_id == organization_id,
            )
            .order_by(ForensicArtifact.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        artifact: ForensicArtifact,
    ) -> ForensicArtifact:
        db.add(artifact)
        await db.flush()
        await db.refresh(artifact)
        return artifact
