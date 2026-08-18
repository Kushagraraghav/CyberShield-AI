"""Evidence integrity verification repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence_integrity import EvidenceIntegrityVerification


class EvidenceIntegrityRepository:
    """Repository for evidence integrity verification operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        **data,
    ) -> EvidenceIntegrityVerification:
        """Create an integrity verification record."""

        verification = EvidenceIntegrityVerification(**data)

        self.session.add(verification)
        await self.session.commit()
        await self.session.refresh(verification)

        return verification

    async def get_by_id(
        self,
        verification_id: UUID,
    ) -> EvidenceIntegrityVerification | None:
        """Get an integrity verification by ID."""

        result = await self.session.execute(
            select(EvidenceIntegrityVerification).where(
                EvidenceIntegrityVerification.id == verification_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_evidence(
        self,
        evidence_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[EvidenceIntegrityVerification]:
        """Get integrity verification records for evidence."""

        result = await self.session.execute(
            select(EvidenceIntegrityVerification)
            .where(
                EvidenceIntegrityVerification.evidence_id == evidence_id
            )
            .order_by(
                EvidenceIntegrityVerification.verified_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def get_latest_by_evidence(
        self,
        evidence_id: UUID,
    ) -> EvidenceIntegrityVerification | None:
        """Get the latest integrity verification for evidence."""

        result = await self.session.execute(
            select(EvidenceIntegrityVerification)
            .where(
                EvidenceIntegrityVerification.evidence_id == evidence_id
            )
            .order_by(
                EvidenceIntegrityVerification.verified_at.desc()
            )
            .limit(1)
        )

        return result.scalar_one_or_none()
