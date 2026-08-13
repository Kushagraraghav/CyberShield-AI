"""ThreatIndicator model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ThreatIndicator(Base):
    """Threat indicator entity for threat intelligence."""

    __tablename__ = "threat_indicators"
    __table_args__ = (
        Index("idx_organization_id", "organization_id"),
        Index("idx_indicator_type", "indicator_type"),
        Index("idx_indicator_value", "indicator_value"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    indicator_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # ip, domain, url, hash, email
    indicator_value: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    confidence: Mapped[int] = mapped_column(default=0, nullable=False)  # 0-100
    severity: Mapped[str] = mapped_column(
        String(50), default="medium", nullable=False
    )  # low, medium, high, critical
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="threat_indicators")

    def __repr__(self) -> str:
        return f"<ThreatIndicator(id={self.id}, type={self.indicator_type}, value={self.indicator_value})>"
