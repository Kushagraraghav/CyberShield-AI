"""Case model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Case(Base):
    """Case entity for investigations."""

    __tablename__ = "cases"
    __table_args__ = (
        Index("idx_organization_id", "organization_id"),
        Index("idx_status", "status"),
        Index("idx_priority", "priority"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    case_number: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="open", nullable=False
    )  # open, investigating, closed, archived
    priority: Mapped[str] = mapped_column(
        String(50), default="medium", nullable=False
    )  # low, medium, high, critical
    created_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="cases")
    created_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="created_cases", foreign_keys=[created_by]
    )
    incidents: Mapped[list["Incident"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )
    evidence: Mapped[list["Evidence"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Case(id={self.id}, case_number={self.case_number}, title={self.title})>"
