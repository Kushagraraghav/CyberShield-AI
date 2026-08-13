"""User service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserService:
    """Service for user business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize UserService with a database session."""
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user.

        Args:
            user_data: User creation schema

        Returns:
            UserResponse schema
        """
        # Create user with hashed password (placeholder - real hashing in Phase 4)
        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["password_hash"] = f"hashed_{password}"  # TODO: Use bcrypt in Phase 4

        user = await self.repository.create(**user_dict)
        return UserResponse.model_validate(user)

    async def get_user(self, user_id) -> UserResponse | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            UserResponse schema or None
        """
        user = await self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user) if user else None

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        """Get user by email.

        Args:
            email: User email

        Returns:
            UserResponse schema or None
        """
        user = await self.repository.get_by_email(email)
        return UserResponse.model_validate(user) if user else None

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        """Get user by username.

        Args:
            username: User username

        Returns:
            UserResponse schema or None
        """
        user = await self.repository.get_by_username(username)
        return UserResponse.model_validate(user) if user else None

    async def update_user(self, user_id, update_data: UserUpdate) -> UserResponse | None:
        """Update user.

        Args:
            user_id: User ID
            update_data: User update schema

        Returns:
            Updated UserResponse schema or None
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        user = await self.repository.update(user_id, **update_dict)
        return UserResponse.model_validate(user) if user else None

    async def delete_user(self, user_id) -> bool:
        """Delete user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(user_id)

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Get all active users.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of active users
        """
        users = await self.repository.get_active_users(skip, limit)
        return [UserResponse.model_validate(user) for user in users]
