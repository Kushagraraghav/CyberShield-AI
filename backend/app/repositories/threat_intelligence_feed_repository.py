"""Threat intelligence feed repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.threat_intelligence_feed import ThreatIntelligenceFeed
from app.repositories.base_repository import BaseRepository


class ThreatIntelligenceFeedRepository(
    BaseRepository[ThreatIntelligenceFeed]
):
    """Repository for ThreatIntelligenceFeed model."""

    def __init__(self, session: Session):
        super().__init__(session, ThreatIntelligenceFeed)

    def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIntelligenceFeed]:
        """Get feeds belonging to an organization."""

        stmt = (
            select(ThreatIntelligenceFeed)
            .where(
                ThreatIntelligenceFeed.organization_id
                == organization_id
            )
            .offset(skip)
            .limit(limit)
        )

        return list(self.session.scalars(stmt).all())

    def get_active_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIntelligenceFeed]:
        """Get active feeds belonging to an organization."""

        stmt = (
            select(ThreatIntelligenceFeed)
            .where(
                ThreatIntelligenceFeed.organization_id
                == organization_id,
                ThreatIntelligenceFeed.is_active.is_(True),
            )
            .offset(skip)
            .limit(limit)
        )

        return list(self.session.scalars(stmt).all())

    def get_by_id_and_organization(
        self,
        feed_id: UUID,
        organization_id: UUID,
    ) -> ThreatIntelligenceFeed | None:
        """Get a feed while enforcing organization isolation."""

        stmt = select(ThreatIntelligenceFeed).where(
            ThreatIntelligenceFeed.id == feed_id,
            ThreatIntelligenceFeed.organization_id == organization_id,
        )

        return self.session.scalars(stmt).first()
