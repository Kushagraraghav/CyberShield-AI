"""Case repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case
from app.repositories.base_repository import BaseRepository


class CaseRepository(BaseRepository[Case]):
    """Repository for Case model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize CaseRepository."""
        super().__init__(session, Case)

    async def get_by_case_number_and_org(
        self, case_number: str, organization_id: UUID
    ) -> Case | None:
        """Get case by case number within an organization.

        Args:
            case_number: Case number
            organization_id: Organization ID

        Returns:
            Case instance or None if not found
        """
        stmt = select(Case).where(
            (Case.case_number == case_number) & (Case.organization_id == organization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Case]:
        """Get all cases in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases
        """
        stmt = (
            select(Case)
            .where(Case.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Case]:
        """Get all cases with a specific status in an organization.

        Args:
            status: Case status (open, investigating, closed, archived)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases with specified status
        """
        stmt = (
            select(Case)
            .where((Case.status == status) & (Case.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_priority(
        self, priority: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Case]:
        """Get all cases with a specific priority in an organization.

        Args:
            priority: Case priority (low, medium, high, critical)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of cases with specified priority
        """
        stmt = (
            select(Case)
            .where((Case.priority == priority) & (Case.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
