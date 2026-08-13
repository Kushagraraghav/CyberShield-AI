"""Alert service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse


class AlertService:
    """Service for alert business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize AlertService with a database session."""
        self.repository = AlertRepository(session)

    async def create_alert(self, alert_data: AlertCreate) -> AlertResponse:
        """Create a new alert.

        Args:
            alert_data: Alert creation schema

        Returns:
            AlertResponse schema
        """
        alert = await self.repository.create(**alert_data.model_dump())
        return AlertResponse.model_validate(alert)

    async def get_alert(self, alert_id: UUID) -> AlertResponse | None:
        """Get alert by ID.

        Args:
            alert_id: Alert ID

        Returns:
            AlertResponse schema or None
        """
        alert = await self.repository.get_by_id(alert_id)
        return AlertResponse.model_validate(alert) if alert else None

    async def update_alert(self, alert_id: UUID, update_data: AlertUpdate) -> AlertResponse | None:
        """Update alert.

        Args:
            alert_id: Alert ID
            update_data: Alert update schema

        Returns:
            Updated AlertResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        alert = await self.repository.update(alert_id, **update_dict)
        return AlertResponse.model_validate(alert) if alert else None

    async def delete_alert(self, alert_id: UUID) -> bool:
        """Delete alert.

        Args:
            alert_id: Alert ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(alert_id)

    async def get_alerts_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AlertResponse]:
        """Get all alerts in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts
        """
        alerts = await self.repository.get_by_organization(organization_id, skip, limit)
        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_alerts_by_incident(
        self, incident_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AlertResponse]:
        """Get all alerts for an incident.

        Args:
            incident_id: Incident ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts for the incident
        """
        alerts = await self.repository.get_by_incident(incident_id, skip, limit)
        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_alerts_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AlertResponse]:
        """Get all alerts with a specific severity.

        Args:
            severity: Alert severity
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts with specified severity
        """
        alerts = await self.repository.get_by_severity(severity, organization_id, skip, limit)
        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_alerts_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AlertResponse]:
        """Get all alerts with a specific status.

        Args:
            status: Alert status
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of alerts with specified status
        """
        alerts = await self.repository.get_by_status(status, organization_id, skip, limit)
        return [AlertResponse.model_validate(alert) for alert in alerts]

    async def get_unacknowledged_alerts(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AlertResponse]:
        """Get all unacknowledged alerts in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of unacknowledged alerts
        """
        alerts = await self.repository.get_unacknowledged(organization_id, skip, limit)
        return [AlertResponse.model_validate(alert) for alert in alerts]
