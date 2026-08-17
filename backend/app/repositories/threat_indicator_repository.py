"""Threat indicator repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.threat_indicator import ThreatIndicator
from app.repositories.base_repository import BaseRepository


class ThreatIndicatorRepository(BaseRepository[ThreatIndicator]):
    """Repository for ThreatIndicator model with custom queries."""

    def __init__(self, session: AsyncSession):
        """Initialize ThreatIndicatorRepository."""
        super().__init__(session, ThreatIndicator)

    async def get_by_organization(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIndicator]:
        """Get all threat indicators in an organization."""
        stmt = (
            select(ThreatIndicator)
            .where(
                ThreatIndicator.organization_id == organization_id
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_type(
        self,
        indicator_type: str,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIndicator]:
        """Get threat indicators of a specific type."""
        stmt = (
            select(ThreatIndicator)
            .where(
                ThreatIndicator.indicator_type == indicator_type,
                ThreatIndicator.organization_id == organization_id,
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_value(
        self,
        indicator_value: str,
        organization_id: UUID,
    ) -> list[ThreatIndicator]:
        """Get threat indicators by exact value."""
        stmt = select(ThreatIndicator).where(
            ThreatIndicator.indicator_value == indicator_value,
            ThreatIndicator.organization_id == organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIndicator]:
        """Get all active threat indicators."""
        stmt = (
            select(ThreatIndicator)
            .where(
                ThreatIndicator.is_active.is_(True),
                ThreatIndicator.organization_id == organization_id,
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_severity(
        self,
        severity: str,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIndicator]:
        """Get threat indicators with a specific severity."""
        stmt = (
            select(ThreatIndicator)
            .where(
                ThreatIndicator.severity == severity,
                ThreatIndicator.organization_id == organization_id,
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search(
        self,
        organization_id: UUID,
        search_term: str | None = None,
        indicator_type: str | None = None,
        severity: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ThreatIndicator]:
        """Search threat indicators within an organization."""

        conditions = [
            ThreatIndicator.organization_id == organization_id
        ]

        if search_term:
            conditions.append(
                ThreatIndicator.indicator_value.ilike(
                    f"%{search_term}%"
                )
            )

        if indicator_type:
            conditions.append(
                ThreatIndicator.indicator_type == indicator_type
            )

        if severity:
            conditions.append(
                ThreatIndicator.severity == severity
            )

        if is_active is not None:
            conditions.append(
                ThreatIndicator.is_active == is_active
            )

        stmt = (
            select(ThreatIndicator)
            .where(*conditions)
            .order_by(ThreatIndicator.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()
