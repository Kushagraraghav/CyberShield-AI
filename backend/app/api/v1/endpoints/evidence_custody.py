from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.evidence_custody import (
    EvidenceCustodyCreate,
    EvidenceCustodyResponse,
)
from app.services.evidence_custody_service import EvidenceCustodyService
from app.api.v1.dependencies import require_evidence_analyst, require_evidence_viewer
from app.models.user import User


router = APIRouter(
    prefix="/evidence-custody",
    tags=["Evidence Custody"],
)


@router.post(
    "",
    response_model=EvidenceCustodyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_custody_record(
    payload: EvidenceCustodyCreate,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    return await EvidenceCustodyService.create_custody_record(
        db=db,
        evidence_id=payload.evidence_id,
        organization_id=payload.organization_id,
        action=payload.action,
        from_holder=payload.from_holder,
        to_holder=payload.to_holder,
        location=payload.location,
        notes=payload.notes,
        integrity_hash=payload.integrity_hash,
        timestamp=payload.timestamp,
    )


@router.get(
    "/evidence/{evidence_id}",
    response_model=list[EvidenceCustodyResponse],
)
async def list_evidence_custody(
    evidence_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    records = await EvidenceCustodyService.list_evidence_custody(
        db=db,
        evidence_id=evidence_id,
        organization_id=organization_id,
    )

    return list(records)


@router.get(
    "/{custody_id}",
    response_model=EvidenceCustodyResponse,
)
async def get_custody_record(
    custody_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    record = await EvidenceCustodyService.get_custody_record(
        db=db,
        custody_id=custody_id,
        organization_id=organization_id,
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence custody record not found",
        )

    return record



