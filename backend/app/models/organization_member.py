"""OrganizationMember model - association between User and Organization."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrganizationMember(Base):
    """Organization membership with roles."""

    __tablename__ = "organization_members"
    __table_args__ = (
        UniqueConstraint("user_id", "organization_id", name="uc_user_org"),
        Index("idx_organization_id", "organization_id"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(50), default="analyst", nullable=False
    )  # admin, analyst, investigator, viewer
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="organization_members")
    organization: Mapped["Organization"] = relationship(back_populates="members")

    def __repr__(self) -> str:
        return f"<OrganizationMember(user_id={self.user_id}, organization_id={self.organization_id}, role={self.role})>"
