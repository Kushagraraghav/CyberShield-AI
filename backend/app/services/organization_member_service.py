"""Organization member service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.organization_member_repository import OrganizationMemberRepository
from app.schemas.organization_member import (
    OrganizationMemberCreate,
    OrganizationMemberUpdate,
    OrganizationMemberResponse,
)


class OrganizationMemberService:
    """Service for organization member business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize OrganizationMemberService with a database session."""
        self.repository = OrganizationMemberRepository(session)

    async def create_member(self, member_data: OrganizationMemberCreate) -> OrganizationMemberResponse:
        """Create a new organization member.

        Args:
            member_data: Organization member creation schema

        Returns:
            OrganizationMemberResponse schema
        """
        member = await self.repository.create(**member_data.model_dump())
        return OrganizationMemberResponse.model_validate(member)

    async def get_member(self, member_id: UUID) -> OrganizationMemberResponse | None:
        """Get organization member by ID.

        Args:
            member_id: Member ID

        Returns:
            OrganizationMemberResponse schema or None
        """
        member = await self.repository.get_by_id(member_id)
        return OrganizationMemberResponse.model_validate(member) if member else None

    async def get_member_by_user_and_org(
        self, user_id: UUID, organization_id: UUID
    ) -> OrganizationMemberResponse | None:
        """Get organization member by user and organization.

        Args:
            user_id: User ID
            organization_id: Organization ID

        Returns:
            OrganizationMemberResponse schema or None
        """
        member = await self.repository.get_by_user_and_org(user_id, organization_id)
        return OrganizationMemberResponse.model_validate(member) if member else None

    async def update_member(
        self, member_id: UUID, update_data: OrganizationMemberUpdate
    ) -> OrganizationMemberResponse | None:
        """Update organization member.

        Args:
            member_id: Member ID
            update_data: Organization member update schema

        Returns:
            Updated OrganizationMemberResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        member = await self.repository.update(member_id, **update_dict)
        return OrganizationMemberResponse.model_validate(member) if member else None

    async def delete_member(self, member_id: UUID) -> bool:
        """Delete organization member.

        Args:
            member_id: Member ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(member_id)

    async def get_members_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[OrganizationMemberResponse]:
        """Get all members of an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of organization members
        """
        members = await self.repository.get_members_by_organization(organization_id, skip, limit)
        return [OrganizationMemberResponse.model_validate(member) for member in members]

    async def get_organizations_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[OrganizationMemberResponse]:
        """Get all organizations a user is member of.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of organization memberships
        """
        memberships = await self.repository.get_organizations_by_user(user_id, skip, limit)
        return [OrganizationMemberResponse.model_validate(m) for m in memberships]
