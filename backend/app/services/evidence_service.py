"""Evidence service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.evidence_repository import EvidenceRepository
from app.schemas.evidence import EvidenceCreate, EvidenceUpdate, EvidenceResponse


class EvidenceService:
    """Service for evidence business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize EvidenceService with a database session."""
        self.repository = EvidenceRepository(session)

    async def create_evidence(self, evidence_data: EvidenceCreate) -> EvidenceResponse:
        """Create a new evidence item.

        Args:
            evidence_data: Evidence creation schema

        Returns:
            EvidenceResponse schema
        """
        evidence = await self.repository.create(**evidence_data.model_dump())
        return EvidenceResponse.model_validate(evidence)

    async def get_evidence(self, evidence_id: UUID) -> EvidenceResponse | None:
        """Get evidence by ID.

        Args:
            evidence_id: Evidence ID

        Returns:
            EvidenceResponse schema or None
        """
        evidence = await self.repository.get_by_id(evidence_id)
        return EvidenceResponse.model_validate(evidence) if evidence else None

    async def update_evidence(
        self, evidence_id: UUID, update_data: EvidenceUpdate
    ) -> EvidenceResponse | None:
        """Update evidence.

        Args:
            evidence_id: Evidence ID
            update_data: Evidence update schema

        Returns:
            Updated EvidenceResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        evidence = await self.repository.update(evidence_id, **update_dict)
        return EvidenceResponse.model_validate(evidence) if evidence else None

    async def delete_evidence(self, evidence_id: UUID) -> bool:
        """Delete evidence.

        Args:
            evidence_id: Evidence ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(evidence_id)

    async def get_evidence_by_case(
        self, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[EvidenceResponse]:
        """Get all evidence for a case.

        Args:
            case_id: Case ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence
        """
        evidence_list = await self.repository.get_by_case(case_id, skip, limit)
        return [EvidenceResponse.model_validate(e) for e in evidence_list]

    async def get_evidence_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[EvidenceResponse]:
        """Get all evidence in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence
        """
        evidence_list = await self.repository.get_by_organization(organization_id, skip, limit)
        return [EvidenceResponse.model_validate(e) for e in evidence_list]

    async def get_evidence_by_sha256(
        self, sha256_hash: str, organization_id: UUID
    ) -> list[EvidenceResponse]:
        """Get evidence by SHA256 hash within an organization.

        Args:
            sha256_hash: SHA256 hash value
            organization_id: Organization ID

        Returns:
            List of evidence with the specified hash
        """
        evidence_list = await self.repository.get_by_sha256_hash(sha256_hash, organization_id)
        return [EvidenceResponse.model_validate(e) for e in evidence_list]

    async def get_evidence_by_type(
        self, evidence_type: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[EvidenceResponse]:
        """Get evidence of a specific type in an organization.

        Args:
            evidence_type: Evidence type
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of evidence with specified type
        """
        evidence_list = await self.repository.get_by_type(evidence_type, organization_id, skip, limit)
        return [EvidenceResponse.model_validate(e) for e in evidence_list]

    async def get_evidence_by_number(
        self, evidence_number: str, case_id: UUID
    ) -> EvidenceResponse | None:
        """Get evidence by evidence number within a case.

        Args:
            evidence_number: Evidence number
            case_id: Case ID

        Returns:
            EvidenceResponse schema or None
        """
        evidence = await self.repository.get_by_evidence_number(evidence_number, case_id)
        return EvidenceResponse.model_validate(evidence) if evidence else None
