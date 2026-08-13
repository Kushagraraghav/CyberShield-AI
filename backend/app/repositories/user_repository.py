"""User repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize UserRepository."""
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email.

        Args:
            email: User email address

        Returns:
            User instance or None if not found
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        """Get user by username.

        Args:
            username: User username

        Returns:
            User instance or None if not found
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        stmt = select(User).where(User.is_active == True).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
