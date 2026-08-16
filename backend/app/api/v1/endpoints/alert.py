"""Alert API endpoints."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_viewer, require_analyst
from app.db.session import get_db
from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """Create a new alert."""

    alert = Alert(
        id=uuid4(),
        organization_id=alert_data.organization_id,
        incident_id=alert_data.incident_id,
        title=alert_data.title,
        description=alert_data.description,
        severity=alert_data.severity,
        status=alert_data.status,
        source=alert_data.source,
        source_event_id=alert_data.source_event_id,
        detected_at=alert_data.detected_at,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


@router.get(
    "",
    response_model=list[AlertResponse],
)
def list_alerts(
    organization_id: UUID | None = None,
    incident_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer),
):
    """List alerts with optional organization and incident filters."""

    if organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="organization_id is required",
        )

    query = (
        select(Alert)
        .where(Alert.organization_id == organization_id)
        .order_by(Alert.created_at.desc())
    )

    if incident_id is not None:
        query = query.where(Alert.incident_id == incident_id)

    alerts = db.scalars(query).all()

    return list(alerts)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer),
):
    """Return an alert by ID."""

    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


@router.patch(
    "/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: UUID,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """Update an alert."""

    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    update_data = alert_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(alert, field, value)

    if alert.status == "acknowledged" and alert.acknowledged_at is None:
        alert.acknowledged_at = datetime.now(timezone.utc)

    if alert.status in {"resolved", "dismissed"} and alert.resolved_at is None:
        alert.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert


@router.delete(
    "/{alert_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """Delete an alert."""

    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    db.delete(alert)
    db.commit()

    return None
