"""Case service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.case_repository import CaseRepository
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse


class CaseService:
    """Service for case business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize CaseService with a database session."""
        self.repository = CaseRepository(session)

    async def create_case(self, case_data: CaseCreate) -> CaseResponse:
        """Create a new case.

        Args:
            case_data: Case creation schema

        Returns:
            CaseResponse schema
        """
        case = await self.repository.create(**case_data.model_dump())
        return CaseResponse.model_validate(case)

    async def get_case(self, case_id: UUID) -> CaseResponse | None:
        """Get case by ID.

        Args:
            case_id: Case ID

        Returns:
            CaseResponse schema or None
        """
        case = await self.repository.get_by_id(case_id)
        return CaseResponse.model_validate(case) if case else None

    async def get_case_by_case_number(
        self, case_number: str, organization_id: UUID
    ) -> CaseResponse | None:
        """Get case by case number within an organization.

        Args:
            case_number: Case number
            organization_id: Organization ID

        Returns:
            CaseResponse schema or None
        """
        case = await self.repository.get_by_case_number_and_org(case_number, organization_id)
        return CaseResponse.model_validate(case) if case else None

    async def update_case(self, case_id: UUID, update_data: CaseUpdate) -> CaseResponse | None:
        """Update case.

        Args:
            case_id: Case ID
            update_data: Case update schema

        Returns:
            Updated CaseResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        case = await self.repository.update(case_id, **update_dict)
        return CaseResponse.model_validate(case) if case else None

    async def delete_case(self, case_id: UUID) -> bool:
        """Delete case.

        Args:
            case_id: Case ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(case_id)

    async def get_cases_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[CaseResponse]:
        """Get all cases in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases
        """
        cases = await self.repository.get_by_organization(organization_id, skip, limit)
        return [CaseResponse.model_validate(case) for case in cases]

    async def get_cases_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[CaseResponse]:
        """Get all cases with a specific status.

        Args:
            status: Case status
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases with specified status
        """
        cases = await self.repository.get_by_status(status, organization_id, skip, limit)
        return [CaseResponse.model_validate(case) for case in cases]

    async def get_cases_by_priority(
        self, priority: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[CaseResponse]:
        """Get all cases with a specific priority.

        Args:
            priority: Case priority
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases with specified priority
        """
        cases = await self.repository.get_by_priority(priority, organization_id, skip, limit)
        return [CaseResponse.model_validate(case) for case in cases]
