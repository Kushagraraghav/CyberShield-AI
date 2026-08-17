"""Threat intelligence feed API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_organization_role
from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.threat_intelligence_feed import ThreatIntelligenceFeed
from app.models.user import User
from app.schemas.threat_intelligence_feed import (
    ThreatIntelligenceFeedCreate,
    ThreatIntelligenceFeedResponse,
    ThreatIntelligenceFeedUpdate,
)
from app.services.threat_intelligence_feed_service import (
    ThreatIntelligenceFeedService,
)

router = APIRouter(
    prefix="/threat-intelligence-feeds",
    tags=["Threat Intelligence Feeds"],
)


@router.post(
    "",
    response_model=ThreatIntelligenceFeedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_threat_intelligence_feed(
    feed_data: ThreatIntelligenceFeedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a threat intelligence feed."""

    require_organization_role(
        organization_id=feed_data.organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

    service = ThreatIntelligenceFeedService(db)

    return service.create(feed_data)


@router.get(
    "",
    response_model=list[ThreatIntelligenceFeedResponse],
)
def list_threat_intelligence_feeds(
    organization_id: UUID,
    active_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List threat intelligence feeds for an organization."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )

    service = ThreatIntelligenceFeedService(db)

    return service.list_by_organization(
        organization_id=organization_id,
        skip=skip,
        limit=limit,
        active_only=active_only,
    )


@router.get(
    "/{feed_id}",
    response_model=ThreatIntelligenceFeedResponse,
)
def get_threat_intelligence_feed(
    feed_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a threat intelligence feed."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )

    service = ThreatIntelligenceFeedService(db)

    feed = service.get_by_id(
        feed_id=feed_id,
        organization_id=organization_id,
    )

    if feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat intelligence feed not found",
        )

    return feed


@router.patch(
    "/{feed_id}",
    response_model=ThreatIntelligenceFeedResponse,
)
def update_threat_intelligence_feed(
    feed_id: UUID,
    feed_data: ThreatIntelligenceFeedUpdate,
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a threat intelligence feed."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

    service = ThreatIntelligenceFeedService(db)

    feed = service.get_by_id(
        feed_id=feed_id,
        organization_id=organization_id,
    )

    if feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat intelligence feed not found",
        )

    return service.update(feed, feed_data)


@router.delete(
    "/{feed_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_threat_intelligence_feed(
    feed_id: UUID,
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a threat intelligence feed."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst"],
        current_user=current_user,
        db=db,
    )

    service = ThreatIntelligenceFeedService(db)

    feed = service.get_by_id(
        feed_id=feed_id,
        organization_id=organization_id,
    )

    if feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat intelligence feed not found",
        )

    service.delete(feed)

    return None
