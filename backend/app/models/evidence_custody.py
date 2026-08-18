"""Evidence chain of custody model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EvidenceCustody(Base):
    """Chain of custody event for digital evidence."""

    __tablename__ = "evidence_custody"

    __table_args__ = (
        Index("idx_custody_evidence_id", "evidence_id"),
        Index("idx_custody_organization_id", "organization_id"),
        Index("idx_custody_performed_by", "performed_by"),
        Index("idx_custody_timestamp", "timestamp"),
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

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    # collected, transferred, accessed, analyzed, returned, disposed

    performed_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    from_holder: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    to_holder: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    integrity_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    evidence: Mapped["Evidence"] = relationship()

    organization: Mapped["Organization"] = relationship()

    performed_by_user: Mapped[Optional["User"]] = relationship(
        foreign_keys=[performed_by],
    )

    def __repr__(self) -> str:
        return (
            f"<EvidenceCustody("
            f"id={self.id}, "
            f"evidence_id={self.evidence_id}, "
            f"action={self.action}"
            f")>"
        )
