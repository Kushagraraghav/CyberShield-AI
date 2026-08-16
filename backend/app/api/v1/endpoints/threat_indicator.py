"""Threat Indicator API endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_indicator_viewer, require_indicator_analyst, require_indicator_org_viewer, require_indicator_org_analyst
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.models.threat_indicator import ThreatIndicator
from app.schemas.threat_indicator import (
    ThreatIndicatorCreate,
    ThreatIndicatorResponse,
    ThreatIndicatorUpdate,
)

router = APIRouter(
    prefix="/threat-indicators",
    tags=["Threat Indicators"],
)


@router.post(
    "",
    response_model=ThreatIndicatorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_threat_indicator(
    indicator_data: ThreatIndicatorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new threat indicator."""

    indicator = ThreatIndicator(
        id=uuid4(),
        organization_id=indicator_data.organization_id,
        indicator_type=indicator_data.indicator_type,
        indicator_value=indicator_data.indicator_value,
        confidence=indicator_data.confidence,
        severity=indicator_data.severity,
        source=indicator_data.source,
        first_seen=indicator_data.first_seen,
    )

    db.add(indicator)
    db.commit()
    db.refresh(indicator)

    return indicator


@router.get(
    "",
    response_model=list[ThreatIndicatorResponse],
)
def list_threat_indicators(
    organization_id: UUID | None = None,
    indicator_type: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List threat indicators with optional filters."""

    query = select(ThreatIndicator).order_by(
        ThreatIndicator.created_at.desc()
    )

    if organization_id is not None:
        query = query.where(
            ThreatIndicator.organization_id == organization_id
        )

    if indicator_type is not None:
        query = query.where(
            ThreatIndicator.indicator_type == indicator_type
        )

    if is_active is not None:
        query = query.where(
            ThreatIndicator.is_active == is_active
        )

    indicators = db.scalars(query).all()

    return list(indicators)


@router.get(
    "/{indicator_id}",
    response_model=ThreatIndicatorResponse,
)
def get_threat_indicator(
    indicator_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a threat indicator by ID."""

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    return indicator


@router.patch(
    "/{indicator_id}",
    response_model=ThreatIndicatorResponse,
)
def update_threat_indicator(
    indicator_id: UUID,
    indicator_data: ThreatIndicatorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a threat indicator."""

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    update_data = indicator_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(indicator, field, value)

    db.commit()
    db.refresh(indicator)

    return indicator


@router.delete(
    "/{indicator_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_threat_indicator(
    indicator_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_indicator_analyst),
):
    """Delete a threat indicator."""

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    db.delete(indicator)
    db.commit()

    return None
