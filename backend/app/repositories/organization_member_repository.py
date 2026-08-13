"""Organization member repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_member import OrganizationMember
from app.repositories.base_repository import BaseRepository


class OrganizationMemberRepository(BaseRepository[OrganizationMember]):
    """Repository for OrganizationMember model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize OrganizationMemberRepository."""
        super().__init__(session, OrganizationMember)

    async def get_by_user_and_org(
        self, user_id: UUID, organization_id: UUID
    ) -> OrganizationMember | None:
        """Get organization member by user and organization.

        Args:
            user_id: User ID
            organization_id: Organization ID

        Returns:
            OrganizationMember instance or None if not found
        """
        stmt = select(OrganizationMember).where(
            (OrganizationMember.user_id == user_id)
            & (OrganizationMember.organization_id == organization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_members_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[OrganizationMember]:
        """Get all members of an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of organization members
        """
        stmt = (
            select(OrganizationMember)
            .where(OrganizationMember.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_organizations_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[OrganizationMember]:
        """Get all organizations a user is member of.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of organization memberships
        """
        stmt = (
            select(OrganizationMember)
            .where(OrganizationMember.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
