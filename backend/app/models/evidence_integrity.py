"""Evidence integrity verification model."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EvidenceIntegrityVerification(Base):
    """Stores integrity verification results for evidence."""

    __tablename__ = "evidence_integrity_verifications"

    __table_args__ = (
        Index("idx_integrity_evidence_id", "evidence_id"),
        Index("idx_integrity_status", "status"),
        Index("idx_integrity_verified_at", "verified_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)

    evidence_id: Mapped[UUID] = mapped_column(
        ForeignKey("evidence.id", ondelete="CASCADE"),
        nullable=False,
    )

    algorithm: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # sha256, md5

    expected_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    calculated_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )  # verified, failed

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    verified_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    evidence: Mapped["Evidence"] = relationship()

    def __repr__(self) -> str:
        return (
            f"<EvidenceIntegrityVerification("
            f"id={self.id}, "
            f"evidence_id={self.evidence_id}, "
            f"algorithm={self.algorithm}, "
            f"status={self.status}"
            f")>"
        )
