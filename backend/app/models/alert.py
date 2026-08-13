"""Alert model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Alert(Base):
    """Alert entity for security events."""

    __tablename__ = "alerts"
    __table_args__ = (
        Index("idx_organization_id", "organization_id"),
        Index("idx_incident_id", "incident_id"),
        Index("idx_severity", "severity"),
        Index("idx_status", "status"),
        Index("idx_detected_at", "detected_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    incident_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    severity: Mapped[str] = mapped_column(
        String(50), default="medium", nullable=False
    )  # low, medium, high, critical
    status: Mapped[str] = mapped_column(
        String(50), default="new", nullable=False
    )  # new, acknowledged, investigating, resolved, dismissed
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    source_event_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="alerts")
    incident: Mapped[Optional["Incident"]] = relationship(back_populates="alerts")

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, title={self.title}, severity={self.severity})>"
