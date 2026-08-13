"""Threat indicator repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.threat_indicator import ThreatIndicator
from app.repositories.base_repository import BaseRepository


class ThreatIndicatorRepository(BaseRepository[ThreatIndicator]):
    """Repository for ThreatIndicator model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize ThreatIndicatorRepository."""
        super().__init__(session, ThreatIndicator)

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicator]:
        """Get all threat indicators in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators
        """
        stmt = (
            select(ThreatIndicator)
            .where(ThreatIndicator.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_type(
        self, indicator_type: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicator]:
        """Get threat indicators of a specific type.

        Args:
            indicator_type: Indicator type (ip, domain, url, hash, email)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators with specified type
        """
        stmt = (
            select(ThreatIndicator)
            .where(
                (ThreatIndicator.indicator_type == indicator_type)
                & (ThreatIndicator.organization_id == organization_id)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_value(
        self, indicator_value: str, organization_id: UUID
    ) -> list[ThreatIndicator]:
        """Get threat indicators by value within an organization.

        Args:
            indicator_value: Indicator value (IP, domain, URL, hash, email)
            organization_id: Organization ID

        Returns:
            List of threat indicators with specified value
        """
        stmt = select(ThreatIndicator).where(
            (ThreatIndicator.indicator_value == indicator_value)
            & (ThreatIndicator.organization_id == organization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicator]:
        """Get all active threat indicators in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active threat indicators
        """
        stmt = (
            select(ThreatIndicator)
            .where(
                (ThreatIndicator.is_active == True) & (ThreatIndicator.organization_id == organization_id)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicator]:
        """Get threat indicators with a specific severity.

        Args:
            severity: Indicator severity (low, medium, high, critical)
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators with specified severity
        """
        stmt = (
            select(ThreatIndicator)
            .where(
                (ThreatIndicator.severity == severity) & (ThreatIndicator.organization_id == organization_id)
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
