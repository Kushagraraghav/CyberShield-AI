"""Incident model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Incident(Base):
    """Incident entity for security events."""

    __tablename__ = "incidents"
    __table_args__ = (
        Index("idx_case_id", "case_id"),
        Index("idx_organization_id", "organization_id"),
        Index("idx_severity", "severity"),
        Index("idx_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    case_id: Mapped[UUID] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="medium", nullable=False
    )  # low, medium, high, critical
    status: Mapped[str] = mapped_column(
        String(50), default="open", nullable=False
    )  # open, investigating, contained, resolved, closed
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship(back_populates="incidents")
    organization: Mapped["Organization"] = relationship(back_populates="incidents")
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Incident(id={self.id}, case_id={self.case_id}, title={self.title})>"
