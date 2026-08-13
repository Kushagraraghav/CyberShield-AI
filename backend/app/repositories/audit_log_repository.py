"""Audit log repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.repositories.base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for AuditLog model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize AuditLogRepository."""
        super().__init__(session, AuditLog)

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AuditLog]:
        """Get all audit logs for an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        stmt = (
            select(AuditLog)
            .where(AuditLog.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
            .order_by(AuditLog.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AuditLog]:
        """Get all audit logs for a user.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        stmt = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(AuditLog.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_action(
        self, action: str, organization_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> list[AuditLog]:
        """Get all audit logs for a specific action.

        Args:
            action: Action name
            organization_id: Optional organization ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the action
        """
        if organization_id:
            stmt = (
                select(AuditLog)
                .where((AuditLog.action == action) & (AuditLog.organization_id == organization_id))
                .offset(skip)
                .limit(limit)
                .order_by(AuditLog.created_at.desc())
            )
        else:
            stmt = (
                select(AuditLog)
                .where(AuditLog.action == action)
                .offset(skip)
                .limit(limit)
                .order_by(AuditLog.created_at.desc())
            )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_resource_type(
        self, resource_type: str, organization_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> list[AuditLog]:
        """Get all audit logs for a specific resource type.

        Args:
            resource_type: Resource type
            organization_id: Optional organization ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the resource type
        """
        if organization_id:
            stmt = (
                select(AuditLog)
                .where(
                    (AuditLog.resource_type == resource_type)
                    & (AuditLog.organization_id == organization_id)
                )
                .offset(skip)
                .limit(limit)
                .order_by(AuditLog.created_at.desc())
            )
        else:
            stmt = (
                select(AuditLog)
                .where(AuditLog.resource_type == resource_type)
                .offset(skip)
                .limit(limit)
                .order_by(AuditLog.created_at.desc())
            )
        result = await self.session.execute(stmt)
        return result.scalars().all()
