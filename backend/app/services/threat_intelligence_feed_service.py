"""Threat intelligence feed service."""

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models.threat_intelligence_feed import ThreatIntelligenceFeed
from app.repositories.threat_intelligence_feed_repository import (
    ThreatIntelligenceFeedRepository,
)
from app.schemas.threat_intelligence_feed import (
    ThreatIntelligenceFeedCreate,
    ThreatIntelligenceFeedUpdate,
)


class ThreatIntelligenceFeedService:
    """Service for threat intelligence feed operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ThreatIntelligenceFeedRepository(db)

    def create(
        self,
        data: ThreatIntelligenceFeedCreate,
    ) -> ThreatIntelligenceFeed:
        """Create a threat intelligence feed."""

        feed = ThreatIntelligenceFeed(
            id=uuid4(),
            organization_id=data.organization_id,
            name=data.name,
            feed_type=data.feed_type,
            source=data.source,
            feed_url=data.feed_url,
            description=data.description,
            is_active=data.is_active,
        )

        self.db.add(feed)
        self.db.commit()
        self.db.refresh(feed)

        return feed

    def get_by_id(
        self,
        feed_id: UUID,
        organization_id: UUID,
    ) -> ThreatIntelligenceFeed | None:
        """Get a feed belonging to an organization."""

        return self.repository.get_by_id_and_organization(
            feed_id=feed_id,
            organization_id=organization_id,
        )

    def list_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> list[ThreatIntelligenceFeed]:
        """List feeds belonging to an organization."""

        if active_only:
            return self.repository.get_active_by_organization(
                organization_id=organization_id,
                skip=skip,
                limit=limit,
            )

        return self.repository.get_by_organization(
            organization_id=organization_id,
            skip=skip,
            limit=limit,
        )

    def update(
        self,
        feed: ThreatIntelligenceFeed,
        data: ThreatIntelligenceFeedUpdate,
    ) -> ThreatIntelligenceFeed:
        """Update a threat intelligence feed."""

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(feed, field, value)

        self.db.commit()
        self.db.refresh(feed)

        return feed

    def delete(
        self,
        feed: ThreatIntelligenceFeed,
    ) -> None:
        """Delete a threat intelligence feed."""

        self.db.delete(feed)
        self.db.commit()
