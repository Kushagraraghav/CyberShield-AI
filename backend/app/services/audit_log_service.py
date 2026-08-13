"""Audit log service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse


class AuditLogService:
    """Service for audit log business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize AuditLogService with a database session."""
        self.repository = AuditLogRepository(session)

    async def create_audit_log(self, log_data: AuditLogCreate) -> AuditLogResponse:
        """Create a new audit log entry.

        Args:
            log_data: Audit log creation schema

        Returns:
            AuditLogResponse schema
        """
        log = await self.repository.create(**log_data.model_dump())
        return AuditLogResponse.model_validate(log)

    async def get_audit_log(self, log_id: UUID) -> AuditLogResponse | None:
        """Get audit log by ID.

        Args:
            log_id: Audit log ID

        Returns:
            AuditLogResponse schema or None
        """
        log = await self.repository.get_by_id(log_id)
        return AuditLogResponse.model_validate(log) if log else None

    async def get_logs_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AuditLogResponse]:
        """Get all audit logs for an organization.

        Args:
            organization_id: Organization ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        logs = await self.repository.get_by_organization(organization_id, skip, limit)
        return [AuditLogResponse.model_validate(log) for log in logs]

    async def get_logs_by_user(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[AuditLogResponse]:
        """Get all audit logs for a user.

        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs
        """
        logs = await self.repository.get_by_user(user_id, skip, limit)
        return [AuditLogResponse.model_validate(log) for log in logs]

    async def get_logs_by_action(
        self, action: str, organization_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> list[AuditLogResponse]:
        """Get all audit logs for a specific action.

        Args:
            action: Action name
            organization_id: Optional organization ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the action
        """
        logs = await self.repository.get_by_action(action, organization_id, skip, limit)
        return [AuditLogResponse.model_validate(log) for log in logs]

    async def get_logs_by_resource_type(
        self, resource_type: str, organization_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> list[AuditLogResponse]:
        """Get all audit logs for a specific resource type.

        Args:
            resource_type: Resource type
            organization_id: Optional organization ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the resource type
        """
        logs = await self.repository.get_by_resource_type(resource_type, organization_id, skip, limit)
        return [AuditLogResponse.model_validate(log) for log in logs]
