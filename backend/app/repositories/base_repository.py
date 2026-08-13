"""Base repository class with CRUD operations."""

from typing import Generic, TypeVar, Type, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Type variable for model classes
ModelT = TypeVar("ModelT", bound=DeclarativeBase)


class BaseRepository(Generic[ModelT]):
    """Base repository with common CRUD operations."""

    def __init__(self, session: AsyncSession, model_class: Type[ModelT]):
        """Initialize repository with session and model class.

        Args:
            session: AsyncSession instance for database operations
            model_class: SQLAlchemy model class to operate on
        """
        self.session = session
        self.model_class = model_class

    async def create(self, **kwargs) -> ModelT:
        """Create a new entity.

        Args:
            **kwargs: Entity attributes

        Returns:
            Created entity instance
        """
        db_obj = self.model_class(**kwargs)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> ModelT | None:
        """Get entity by ID.

        Args:
            id: Entity ID

        Returns:
            Entity instance or None if not found
        """
        return await self.session.get(self.model_class, id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelT]:
        """Get all entities with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of entity instances
        """
        stmt = select(self.model_class).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, id: UUID, **kwargs) -> ModelT | None:
        """Update an entity.

        Args:
            id: Entity ID
            **kwargs: Attributes to update

        Returns:
            Updated entity instance or None if not found
        """
        db_obj = await self.get_by_id(id)
        if db_obj:
            for key, value in kwargs.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            await self.session.flush()
            await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        """Delete an entity.

        Args:
            id: Entity ID

        Returns:
            True if entity was deleted, False if not found
        """
        db_obj = await self.get_by_id(id)
        if db_obj:
            await self.session.delete(db_obj)
            await self.session.flush()
            return True
        return False

    async def delete_all(self) -> int:
        """Delete all entities (use with caution).

        Returns:
            Number of deleted records
        """
        stmt = delete(self.model_class)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
