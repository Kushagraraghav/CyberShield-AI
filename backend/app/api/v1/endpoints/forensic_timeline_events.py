from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.forensic_timeline_event import (
    ForensicTimelineEventCreate,
    ForensicTimelineEventOut,
)
from app.services.forensic_timeline_event_service import (
    ForensicTimelineEventService,
)
from app.api.v1.dependencies import require_case_analyst, require_case_viewer, require_evidence_viewer
from app.models.user import User


router = APIRouter(
    prefix="/forensic-timeline-events",
    tags=["Forensic Timeline"],
)


@router.post(
    "",
    response_model=ForensicTimelineEventOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_timeline_event(
    payload: ForensicTimelineEventCreate,
    organization_id: UUID,
    current_user: User = Depends(require_case_analyst),
    db: AsyncSession = Depends(get_db),
):
    return await ForensicTimelineEventService.create_event(
        db=db,
        organization_id=organization_id,
        case_id=payload.case_id,
        evidence_id=payload.evidence_id,
        event_time=payload.event_time,
        event_type=payload.event_type,
        title=payload.title,
        description=payload.description,
        source=payload.source,
        artifact_id=payload.artifact_id,
        metadata=payload.metadata,
    )


@router.get(
    "/{event_id}",
    response_model=ForensicTimelineEventOut,
)
async def get_timeline_event(
    event_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_case_viewer),
    db: AsyncSession = Depends(get_db),
):
    event = await ForensicTimelineEventService.get_event(
        db=db,
        event_id=event_id,
        organization_id=organization_id,
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic timeline event not found",
        )

    return event


@router.get(
    "/evidence/{evidence_id}",
    response_model=list[ForensicTimelineEventOut],
)
async def list_evidence_timeline(
    evidence_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    return await ForensicTimelineEventService.list_evidence_events(
        db=db,
        evidence_id=evidence_id,
        organization_id=organization_id,
    )


@router.get(
    "/case/{case_id}",
    response_model=list[ForensicTimelineEventOut],
)
async def list_case_timeline(
    case_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_case_viewer),
    db: AsyncSession = Depends(get_db),
):
    return await ForensicTimelineEventService.list_case_events(
        db=db,
        case_id=case_id,
        organization_id=organization_id,
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_timeline_event(
    event_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_case_analyst),
    db: AsyncSession = Depends(get_db),
):
    event = await ForensicTimelineEventService.get_event(
        db=db,
        event_id=event_id,
        organization_id=organization_id,
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic timeline event not found",
        )

    await ForensicTimelineEventService.delete_event(
        db=db,
        event=event,
    )


