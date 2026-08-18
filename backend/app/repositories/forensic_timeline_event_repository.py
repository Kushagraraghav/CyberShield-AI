from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forensic_timeline_event import ForensicTimelineEvent


class ForensicTimelineEventRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        event: ForensicTimelineEvent,
    ) -> ForensicTimelineEvent:
        db.add(event)
        await db.flush()
        await db.refresh(event)
        return event

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        event_id: UUID,
        organization_id: UUID,
    ) -> ForensicTimelineEvent | None:
        result = await db.execute(
            select(ForensicTimelineEvent).where(
                ForensicTimelineEvent.id == event_id,
                ForensicTimelineEvent.organization_id == organization_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_by_evidence(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> list[ForensicTimelineEvent]:
        result = await db.execute(
            select(ForensicTimelineEvent)
            .where(
                ForensicTimelineEvent.evidence_id == evidence_id,
                ForensicTimelineEvent.organization_id == organization_id,
            )
            .order_by(ForensicTimelineEvent.event_time.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def list_by_case(
        db: AsyncSession,
        case_id: UUID,
        organization_id: UUID,
    ) -> list[ForensicTimelineEvent]:
        result = await db.execute(
            select(ForensicTimelineEvent)
            .where(
                ForensicTimelineEvent.case_id == case_id,
                ForensicTimelineEvent.organization_id == organization_id,
            )
            .order_by(ForensicTimelineEvent.event_time.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def delete(
        db: AsyncSession,
        event: ForensicTimelineEvent,
    ) -> None:
        await db.delete(event)
        await db.flush()