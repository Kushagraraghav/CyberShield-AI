"""Organization service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse


class OrganizationService:
    """Service for organization business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize OrganizationService with a database session."""
        self.repository = OrganizationRepository(session)

    async def create_organization(self, org_data: OrganizationCreate) -> OrganizationResponse:
        """Create a new organization.

        Args:
            org_data: Organization creation schema

        Returns:
            OrganizationResponse schema
        """
        org = await self.repository.create(**org_data.model_dump())
        return OrganizationResponse.model_validate(org)

    async def get_organization(self, org_id) -> OrganizationResponse | None:
        """Get organization by ID.

        Args:
            org_id: Organization ID

        Returns:
            OrganizationResponse schema or None
        """
        org = await self.repository.get_by_id(org_id)
        return OrganizationResponse.model_validate(org) if org else None

    async def get_organization_by_name(self, name: str) -> OrganizationResponse | None:
        """Get organization by name.

        Args:
            name: Organization name

        Returns:
            OrganizationResponse schema or None
        """
        org = await self.repository.get_by_name(name)
        return OrganizationResponse.model_validate(org) if org else None

    async def update_organization(
        self, org_id, update_data: OrganizationUpdate
    ) -> OrganizationResponse | None:
        """Update organization.

        Args:
            org_id: Organization ID
            update_data: Organization update schema

        Returns:
            Updated OrganizationResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        org = await self.repository.update(org_id, **update_dict)
        return OrganizationResponse.model_validate(org) if org else None

    async def delete_organization(self, org_id) -> bool:
        """Delete organization.

        Args:
            org_id: Organization ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(org_id)

    async def get_active_organizations(self, skip: int = 0, limit: int = 100) -> list[OrganizationResponse]:
        """Get all active organizations.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active organizations
        """
        orgs = await self.repository.get_active_organizations(skip, limit)
        return [OrganizationResponse.model_validate(org) for org in orgs]
