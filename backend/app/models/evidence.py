"""Evidence model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Evidence(Base):
    """Evidence entity for digital forensics."""

    __tablename__ = "evidence"
    __table_args__ = (
        Index("idx_case_id", "case_id"),
        Index("idx_organization_id", "organization_id"),
        Index("idx_sha256_hash", "sha256_hash"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    case_id: Mapped[UUID] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    evidence_number: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    evidence_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # disk_image, memory_dump, log, document, network_capture, executable, other
    file_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    sha256_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    md5_hash: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    storage_path: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    collected_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(back_populates="evidence")
    organization: Mapped["Organization"] = relationship(back_populates="evidence")
    collected_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="collected_evidence", foreign_keys=[collected_by]
    )

    def __repr__(self) -> str:
        return f"<Evidence(id={self.id}, evidence_number={self.evidence_number}, name={self.name})>"
