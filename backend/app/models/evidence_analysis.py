"""Evidence analysis model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EvidenceAnalysis(Base):
    """Analysis performed on digital evidence."""

    __tablename__ = "evidence_analyses"
    __table_args__ = (
        Index("idx_analysis_evidence_id", "evidence_id"),
        Index("idx_analysis_organization_id", "organization_id"),
        Index("idx_analysis_type", "analysis_type"),
        Index("idx_analysis_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)

    evidence_id: Mapped[UUID] = mapped_column(
        ForeignKey("evidence.id", ondelete="CASCADE"),
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    analysis_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # metadata, filesystem, malware, network, memory, log, timeline, other

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )
    # pending, in_progress, completed, failed

    findings: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    tool_used: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    analyst_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    analyzed_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
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

    # Relationships
    evidence: Mapped["Evidence"] = relationship(
        back_populates="analyses"
    )

    organization: Mapped["Organization"] = relationship()

    analyzed_by_user: Mapped[Optional["User"]] = relationship(
        foreign_keys=[analyzed_by]
    )

    def __repr__(self) -> str:
        return (
            f"<EvidenceAnalysis("
            f"id={self.id}, "
            f"evidence_id={self.evidence_id}, "
            f"type={self.analysis_type}, "
            f"status={self.status})>"
        )
