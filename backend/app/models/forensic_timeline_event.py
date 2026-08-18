from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ForensicTimelineEvent(Base):
    """Timeline event extracted from digital forensic evidence."""

    __tablename__ = "forensic_timeline_events"

    __table_args__ = (
        Index("idx_timeline_case_id", "case_id"),
        Index("idx_timeline_evidence_id", "evidence_id"),
        Index("idx_timeline_organization_id", "organization_id"),
        Index("idx_timeline_event_time", "event_time"),
        Index("idx_timeline_event_type", "event_type"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)

    case_id: Mapped[UUID] = mapped_column(
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False,
    )

    evidence_id: Mapped[UUID] = mapped_column(
        ForeignKey("evidence.id", ondelete="CASCADE"),
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # file_created, file_modified, file_accessed, process,
    # network, login, email, browser, registry, other

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    artifact_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("forensic_artifacts.id", ondelete="SET NULL"),
        nullable=True,
    )

    event_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    case: Mapped["Case"] = relationship()

    evidence: Mapped["Evidence"] = relationship()

    organization: Mapped["Organization"] = relationship()

    artifact: Mapped[Optional["ForensicArtifact"]] = relationship()

    def __repr__(self) -> str:
        return (
            f"<ForensicTimelineEvent("
            f"id={self.id}, "
            f"evidence_id={self.evidence_id}, "
            f"event_type={self.event_type}, "
            f"event_time={self.event_time})>"
        )
