from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ForensicArtifact(Base):
    """Forensic artifact extracted or identified from digital evidence."""

    __tablename__ = "forensic_artifacts"
    __table_args__ = (
        Index("idx_artifact_evidence_id", "evidence_id"),
        Index("idx_artifact_organization_id", "organization_id"),
        Index("idx_artifact_type", "artifact_type"),
        Index("idx_artifact_name", "name"),
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

    artifact_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # file, browser, registry, email, process, network, log, timeline, other

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    path: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    hash_value: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="identified",
        nullable=False,
    )
    # identified, extracted, analyzed, flagged, dismissed

    discovered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
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

    evidence: Mapped["Evidence"] = relationship(
        back_populates="artifacts"
    )

    organization: Mapped["Organization"] = relationship()

    def __repr__(self) -> str:
        return (
            f"<ForensicArtifact("
            f"id={self.id}, "
            f"evidence_id={self.evidence_id}, "
            f"type={self.artifact_type}, "
            f"name={self.name}, "
            f"status={self.status})>"
        )
