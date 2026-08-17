"""Threat intelligence feed model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ThreatIntelligenceFeed(Base):
    """Threat intelligence feed configuration."""

    __tablename__ = "threat_intelligence_feeds"

    __table_args__ = (
        Index(
            "idx_threat_feed_organization_id",
            "organization_id",
        ),
        Index(
            "idx_threat_feed_is_active",
            "is_active",
        ),
        Index(
            "idx_threat_feed_type",
            "feed_type",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    feed_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # ip, domain, url, hash, mixed

    source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    feed_url: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    last_fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_successful_fetch_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship()

    def __repr__(self) -> str:
        return (
            f"<ThreatIntelligenceFeed("
            f"id={self.id}, "
            f"name={self.name}, "
            f"type={self.feed_type}"
            f")>"
        )
