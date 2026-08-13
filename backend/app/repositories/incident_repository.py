"""Incident repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident
from app.repositories.base_repository import BaseRepository


class IncidentRepository(BaseRepository[Incident]):
    """Repository for Incident model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize IncidentRepository."""
        super().__init__(session, Incident)

    async def get_by_case(
        self, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Incident]:
        """Get all incidents in a case.

        Args:
            case_id: Case ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents
        """
        stmt = (
            select(Incident)
            .where(Incident.case_id == case_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Incident]:
        """Get all incidents in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents
        """
        stmt = (
            select(Incident)
            .where(Incident.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Incident]:
        """Get all incidents with a specific severity.

        Args:
            severity: Incident severity (low, medium, high, critical)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents with specified severity
        """
        stmt = (
            select(Incident)
            .where((Incident.severity == severity) & (Incident.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Incident]:
        """Get all incidents with a specific status.

        Args:
            status: Incident status (open, investigating, contained, resolved, closed)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents with specified status
        """
        stmt = (
            select(Incident)
            .where((Incident.status == status) & (Incident.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
