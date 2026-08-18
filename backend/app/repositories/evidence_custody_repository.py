"""Evidence chain of custody repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence_custody import EvidenceCustody


class EvidenceCustodyRepository:
    """Repository for chain of custody operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **data) -> EvidenceCustody:
        """Create a custody event."""
        custody = EvidenceCustody(**data)

        self.session.add(custody)
        await self.session.commit()
        await self.session.refresh(custody)

        return custody

    async def get_by_id(
        self,
        custody_id: UUID,
    ) -> EvidenceCustody | None:
        """Get a custody event by ID."""
        result = await self.session.execute(
            select(EvidenceCustody).where(
                EvidenceCustody.id == custody_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_evidence(
        self,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> list[EvidenceCustody]:
        """Get custody history for evidence."""
        result = await self.session.execute(
            select(EvidenceCustody)
            .where(
                EvidenceCustody.evidence_id == evidence_id,
                EvidenceCustody.organization_id == organization_id,
            )
            .order_by(EvidenceCustody.timestamp.asc())
        )

        return list(result.scalars().all())
