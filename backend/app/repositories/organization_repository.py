"""Organization repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    """Repository for Organization model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize OrganizationRepository."""
        super().__init__(session, Organization)

    async def get_by_name(self, name: str) -> Organization | None:
        """Get organization by name.

        Args:
            name: Organization name

        Returns:
            Organization instance or None if not found
        """
        stmt = select(Organization).where(Organization.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_organizations(self, skip: int = 0, limit: int = 100) -> list[Organization]:
        """Get all active organizations.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active organizations
        """
        stmt = (
            select(Organization)
            .where(Organization.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
