"""Incident service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate, IncidentResponse


class IncidentService:
    """Service for incident business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize IncidentService with a database session."""
        self.repository = IncidentRepository(session)

    async def create_incident(self, incident_data: IncidentCreate) -> IncidentResponse:
        """Create a new incident.

        Args:
            incident_data: Incident creation schema

        Returns:
            IncidentResponse schema
        """
        incident = await self.repository.create(**incident_data.model_dump())
        return IncidentResponse.model_validate(incident)

    async def get_incident(self, incident_id: UUID) -> IncidentResponse | None:
        """Get incident by ID.

        Args:
            incident_id: Incident ID

        Returns:
            IncidentResponse schema or None
        """
        incident = await self.repository.get_by_id(incident_id)
        return IncidentResponse.model_validate(incident) if incident else None

    async def update_incident(
        self, incident_id: UUID, update_data: IncidentUpdate
    ) -> IncidentResponse | None:
        """Update incident.

        Args:
            incident_id: Incident ID
            update_data: Incident update schema

        Returns:
            Updated IncidentResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        incident = await self.repository.update(incident_id, **update_dict)
        return IncidentResponse.model_validate(incident) if incident else None

    async def delete_incident(self, incident_id: UUID) -> bool:
        """Delete incident.

        Args:
            incident_id: Incident ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(incident_id)

    async def get_incidents_by_case(
        self, case_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[IncidentResponse]:
        """Get all incidents in a case.

        Args:
            case_id: Case ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents
        """
        incidents = await self.repository.get_by_case(case_id, skip, limit)
        return [IncidentResponse.model_validate(incident) for incident in incidents]

    async def get_incidents_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[IncidentResponse]:
        """Get all incidents in an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents
        """
        incidents = await self.repository.get_by_organization(organization_id, skip, limit)
        return [IncidentResponse.model_validate(incident) for incident in incidents]

    async def get_incidents_by_severity(
        self, severity: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[IncidentResponse]:
        """Get all incidents with a specific severity.

        Args:
            severity: Incident severity
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents with specified severity
        """
        incidents = await self.repository.get_by_severity(severity, organization_id, skip, limit)
        return [IncidentResponse.model_validate(incident) for incident in incidents]

    async def get_incidents_by_status(
        self, status: str, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[IncidentResponse]:
        """Get all incidents with a specific status.

        Args:
            status: Incident status
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of incidents with specified status
        """
        incidents = await self.repository.get_by_status(status, organization_id, skip, limit)
        return [IncidentResponse.model_validate(incident) for incident in incidents]
