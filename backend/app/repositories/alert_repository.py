"""Alert repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.repositories.base_repository import BaseRepository


class AlertRepository(BaseRepository[Alert]):
    """Repository for Alert model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize AlertRepository."""
        super().__init__(session, Alert)

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Alert]:
        """Get all alerts in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts
        """
        stmt = (
            select(Alert)
            .where(Alert.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_incident(
        self, incident_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Alert]:
        """Get all alerts for an incident.

        Args:
            incident_id: Incident ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts for the incident
        """
        stmt = (
            select(Alert)
            .where(Alert.incident_id == incident_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Alert]:
        """Get all alerts with a specific severity.

        Args:
            severity: Alert severity (low, medium, high, critical)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts with specified severity
        """
        stmt = (
            select(Alert)
            .where((Alert.severity == severity) & (Alert.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Alert]:
        """Get all alerts with a specific status.

        Args:
            status: Alert status (new, acknowledged, investigating, resolved, dismissed)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts with specified status
        """
        stmt = (
            select(Alert)
            .where((Alert.status == status) & (Alert.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_unacknowledged(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Alert]:
        """Get all unacknowledged alerts in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of unacknowledged alerts
        """
        stmt = (
            select(Alert)
            .where((Alert.acknowledged_at == None) & (Alert.organization_id == organization_id))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
