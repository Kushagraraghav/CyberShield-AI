"""Evidence chain of custody service."""

from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.evidence_custody_repository import (
    EvidenceCustodyRepository,
)
from app.schemas.evidence_custody import (
    EvidenceCustodyCreate,
    EvidenceCustodyResponse,
)


class EvidenceCustodyService:
    """Service for evidence chain of custody operations."""

    def __init__(self, session: AsyncSession):
        self.repository = EvidenceCustodyRepository(session)

    async def create_custody_event(
        self,
        data: EvidenceCustodyCreate,
        performed_by: UUID | None = None,
    ) -> EvidenceCustodyResponse:
        """Create a custody event."""

        custody_data = data.model_dump()
        custody_data["id"] = uuid4()
        custody_data["performed_by"] = performed_by

        custody = await self.repository.create(**custody_data)

        return EvidenceCustodyResponse.model_validate(custody)

    async def get_custody_event(
        self,
        custody_id: UUID,
    ) -> EvidenceCustodyResponse | None:
        """Get a custody event."""

        custody = await self.repository.get_by_id(custody_id)

        if custody is None:
            return None

        return EvidenceCustodyResponse.model_validate(custody)

    async def get_evidence_custody(
        self,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> list[EvidenceCustodyResponse]:
        """Get complete custody history for evidence."""

        custody_events = await self.repository.get_by_evidence(
            evidence_id=evidence_id,
            organization_id=organization_id,
        )

        return [
            EvidenceCustodyResponse.model_validate(event)
            for event in custody_events
        ]
