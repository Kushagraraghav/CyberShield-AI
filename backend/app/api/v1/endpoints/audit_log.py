"""Audit Log API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_audit_log_org_viewer, require_audit_log_viewer
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogResponse

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def list_audit_logs(
    organization_id: UUID,
    user_id: UUID | None = None,
    resource_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_audit_log_org_viewer),
):
    """List audit logs with optional filters."""

    query = select(AuditLog).order_by(
        AuditLog.created_at.desc()
    )

    if organization_id is not None:
        query = query.where(
            AuditLog.organization_id == organization_id
        )

    if user_id is not None:
        query = query.where(
            AuditLog.user_id == user_id
        )

    if resource_type is not None:
        query = query.where(
            AuditLog.resource_type == resource_type
        )

    logs = db.scalars(query).all()

    return list(logs)


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(
    audit_log_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_audit_log_viewer),
):
    """Return an audit log by ID."""

    log = db.get(AuditLog, audit_log_id)

    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found",
        )

    return log






