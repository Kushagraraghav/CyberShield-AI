"""Authorization dependencies for RBAC."""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.organization_member import OrganizationMember
from app.models.user import User


def require_organization_role(
    organization_id: UUID,
    allowed_roles: list[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require the current user to have one of the allowed roles."""

    if current_user.is_superuser:
        return current_user

    member = db.scalar(
        select(OrganizationMember).where(
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.organization_id == organization_id,
        )
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )

    if member.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    return current_user


def require_admin(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require admin access."""

    return require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin"],
        current_user=current_user,
        db=db,
    )


def require_analyst(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require analyst-level access."""

    return require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )


def require_investigator(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require investigator-level access."""

    return require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "investigator"],
        current_user=current_user,
        db=db,
    )


def require_viewer(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require viewer-level access."""

    return require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )

def require_case_viewer(
    case_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require viewer-level access to a case."""

    from app.models.case import Case

    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return require_organization_role(
        organization_id=case.organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )


def require_case_analyst(
    case_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require analyst-level access to a case."""

    from app.models.case import Case

    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return require_organization_role(
        organization_id=case.organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

def require_alert_viewer(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require viewer-level access to an alert."""

    from app.models.alert import Alert

    if current_user.is_superuser:
        return current_user

    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return require_organization_role(
        organization_id=alert.organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )


def require_alert_analyst(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require analyst-level access to an alert."""

    from app.models.alert import Alert

    if current_user.is_superuser:
        return current_user

    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return require_organization_role(
        organization_id=alert.organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

def require_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require superuser access."""

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required",
        )

    return current_user

def require_indicator_viewer(
    indicator_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require viewer-level access to a threat indicator."""

    from app.models.threat_indicator import ThreatIndicator

    if current_user.is_superuser:
        return current_user

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    return require_organization_role(
        organization_id=indicator.organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )


def require_indicator_analyst(
    indicator_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require analyst-level access to a threat indicator."""

    from app.models.threat_indicator import ThreatIndicator

    if current_user.is_superuser:
        return current_user

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    return require_organization_role(
        organization_id=indicator.organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

def require_audit_log_viewer(
    audit_log_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Require viewer-level access to an audit log."""

    from app.models.audit_log import AuditLog

    if current_user.is_superuser:
        return current_user

    audit_log = db.get(AuditLog, audit_log_id)

    if audit_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found",
        )

    return require_organization_role(
        organization_id=audit_log.organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )
