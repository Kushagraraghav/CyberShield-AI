from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forensic_timeline_event import ForensicTimelineEvent
from app.repositories.forensic_timeline_event_repository import (
    ForensicTimelineEventRepository,
)


class ForensicTimelineEventService:

    @staticmethod
    async def create_event(
        db: AsyncSession,
        organization_id: UUID,
        case_id: UUID,
        evidence_id: UUID,
        event_time: datetime,
        event_type: str,
        title: str,
        description: str | None = None,
        source: str | None = None,
        artifact_id: UUID | None = None,
        metadata: dict | None = None,
    ) -> ForensicTimelineEvent:

        event = ForensicTimelineEvent(
            id=uuid4(),
            organization_id=organization_id,
            case_id=case_id,
            evidence_id=evidence_id,
            event_time=event_time,
            event_type=event_type,
            title=title,
            description=description,
            source=source,
            artifact_id=artifact_id,
            event_metadata=metadata,
        )

        return await ForensicTimelineEventRepository.create(
            db=db,
            event=event,
        )

    @staticmethod
    async def get_event(
        db: AsyncSession,
        event_id: UUID,
        organization_id: UUID,
    ) -> ForensicTimelineEvent | None:

        return await ForensicTimelineEventRepository.get_by_id(
            db=db,
            event_id=event_id,
            organization_id=organization_id,
        )

    @staticmethod
    async def list_evidence_events(
        db: AsyncSession,
        evidence_id: UUID,
        organization_id: UUID,
    ) -> list[ForensicTimelineEvent]:

        return await ForensicTimelineEventRepository.list_by_evidence(
            db=db,
            evidence_id=evidence_id,
            organization_id=organization_id,
        )

    @staticmethod
    async def list_case_events(
        db: AsyncSession,
        case_id: UUID,
        organization_id: UUID,
    ) -> list[ForensicTimelineEvent]:

        return await ForensicTimelineEventRepository.list_by_case(
            db=db,
            case_id=case_id,
            organization_id=organization_id,
        )

    @staticmethod
    async def delete_event(
        db: AsyncSession,
        event: ForensicTimelineEvent,
    ) -> None:

        await ForensicTimelineEventRepository.delete(
            db=db,
            event=event,
        )