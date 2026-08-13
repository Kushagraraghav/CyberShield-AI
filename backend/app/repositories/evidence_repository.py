"""Evidence repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence import Evidence
from app.repositories.base_repository import BaseRepository


class EvidenceRepository(BaseRepository[Evidence]):
    """Repository for Evidence model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize EvidenceRepository."""
        super().__init__(session, Evidence)

    async def get_by_case(
        self, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Evidence]:
        """Get all evidence for a case.

        Args:
            case_id: Case ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence
        """
        stmt = (
            select(Evidence)
            .where(Evidence.case_id == case_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Evidence]:
        """Get all evidence in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence
        """
        stmt = (
            select(Evidence)
            .where(Evidence.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_sha256_hash(
        self, sha256_hash: str, organization_id: UUID
    ) -> list[Evidence]:
        """Get evidence by SHA256 hash within an organization.

        Args:
            sha256_hash: SHA256 hash value
            organization_id: Organization ID

        Returns:
            List of evidence with the specified hash
        """
        stmt = select(Evidence).where(
            (Evidence.sha256_hash == sha256_hash) & (Evidence.organization_id == organization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_type(
        self, evidence_type: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Evidence]:
        """Get evidence of a specific type in an organization.

        Args:
            evidence_type: Evidence type (disk_image, memory_dump, log, document, network_capture, executable, other)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence with specified type
        """
        stmt = (
            select(Evidence)
            .where((Evidence.evidence_type == evidence_type) & (Evidence.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_evidence_number(
        self, evidence_number: str, case_id: UUID
    ) -> Evidence | None:
        """Get evidence by evidence number within a case.

        Args:
            evidence_number: Evidence number (unique within case)
            case_id: Case ID

        Returns:
            Evidence instance or None if not found
        """
        stmt = select(Evidence).where(
            (Evidence.evidence_number == evidence_number) & (Evidence.case_id == case_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
