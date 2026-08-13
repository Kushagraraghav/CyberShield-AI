"""Threat indicator service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.threat_indicator_repository import ThreatIndicatorRepository
from app.schemas.threat_indicator import (
    ThreatIndicatorCreate,
    ThreatIndicatorUpdate,
    ThreatIndicatorResponse,
)


class ThreatIndicatorService:
    """Service for threat indicator business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize ThreatIndicatorService with a database session."""
        self.repository = ThreatIndicatorRepository(session)

    async def create_threat_indicator(
        self, indicator_data: ThreatIndicatorCreate
    ) -> ThreatIndicatorResponse:
        """Create a new threat indicator.

        Args:
            indicator_data: Threat indicator creation schema

        Returns:
            ThreatIndicatorResponse schema
        """
        indicator = await self.repository.create(**indicator_data.model_dump())
        return ThreatIndicatorResponse.model_validate(indicator)

    async def get_threat_indicator(self, indicator_id: UUID) -> ThreatIndicatorResponse | None:
        """Get threat indicator by ID.

        Args:
            indicator_id: Threat indicator ID

        Returns:
            ThreatIndicatorResponse schema or None
        """
        indicator = await self.repository.get_by_id(indicator_id)
        return ThreatIndicatorResponse.model_validate(indicator) if indicator else None

    async def update_threat_indicator(
        self, indicator_id: UUID, update_data: ThreatIndicatorUpdate
    ) -> ThreatIndicatorResponse | None:
        """Update threat indicator.

        Args:
            indicator_id: Threat indicator ID
            update_data: Threat indicator update schema

        Returns:
            Updated ThreatIndicatorResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        indicator = await self.repository.update(indicator_id, **update_dict)
        return ThreatIndicatorResponse.model_validate(indicator) if indicator else None

    async def delete_threat_indicator(self, indicator_id: UUID) -> bool:
        """Delete threat indicator.

        Args:
            indicator_id: Threat indicator ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(indicator_id)

    async def get_indicators_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicatorResponse]:
        """Get all threat indicators in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators
        """
        indicators = await self.repository.get_by_organization(organization_id, skip, limit)
        return [ThreatIndicatorResponse.model_validate(i) for i in indicators]

    async def get_indicators_by_type(
        self, indicator_type: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicatorResponse]:
        """Get threat indicators of a specific type.

        Args:
            indicator_type: Indicator type
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators with specified type
        """
        indicators = await self.repository.get_by_type(indicator_type, organization_id, skip, limit)
        return [ThreatIndicatorResponse.model_validate(i) for i in indicators]

    async def get_indicators_by_value(
        self, indicator_value: str, organization_id: UUID
    ) -> list[ThreatIndicatorResponse]:
        """Get threat indicators by value within an organization.

        Args:
            indicator_value: Indicator value
            organization_id: Organization ID

        Returns:
            List of threat indicators with specified value
        """
        indicators = await self.repository.get_by_value(indicator_value, organization_id)
        return [ThreatIndicatorResponse.model_validate(i) for i in indicators]

    async def get_active_indicators(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicatorResponse]:
        """Get all active threat indicators in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active threat indicators
        """
        indicators = await self.repository.get_active(organization_id, skip, limit)
        return [ThreatIndicatorResponse.model_validate(i) for i in indicators]

    async def get_indicators_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[ThreatIndicatorResponse]:
        """Get threat indicators with a specific severity.

        Args:
            severity: Indicator severity
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of threat indicators with specified severity
        """
        indicators = await self.repository.get_by_severity(severity, organization_id, skip, limit)
        return [ThreatIndicatorResponse.model_validate(i) for i in indicators]
