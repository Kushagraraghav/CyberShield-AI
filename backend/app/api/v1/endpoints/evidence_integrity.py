"""Evidence integrity verification API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import get_current_user
from app.api.v1.dependencies import require_organization_role
from app.db.session import get_db
from app.models.user import User
from app.schemas.evidence_integrity import (
    EvidenceIntegrityVerificationResponse,
)
from app.services.evidence_integrity_service import EvidenceIntegrityService


router = APIRouter(
    prefix="/evidence",
    tags=["Evidence Integrity"],
)


@router.post(
    "/{evidence_id}/integrity/verify",
    response_model=EvidenceIntegrityVerificationResponse,
)
async def verify_evidence_integrity(
    evidence_id: UUID,
    organization_id: UUID,
    algorithm: str = "sha256",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Verify the integrity of an evidence file."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator"],
        current_user=current_user,
        db=db,
    )

    service = EvidenceIntegrityService(db)

    try:
        result = await service.verify(
            evidence_id=evidence_id,
            algorithm=algorithm,
            verified_by=current_user.id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    return result


@router.get(
    "/{evidence_id}/integrity/latest",
    response_model=EvidenceIntegrityVerificationResponse,
)
async def get_latest_evidence_integrity(
    evidence_id: UUID,
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the latest integrity verification."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )

    service = EvidenceIntegrityService(db)

    result = await service.get_latest(evidence_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No integrity verification found",
        )

    return result


@router.get(
    "/{evidence_id}/integrity/history",
    response_model=list[EvidenceIntegrityVerificationResponse],
)
async def get_evidence_integrity_history(
    evidence_id: UUID,
    organization_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get integrity verification history."""

    require_organization_role(
        organization_id=organization_id,
        allowed_roles=["admin", "analyst", "investigator", "viewer"],
        current_user=current_user,
        db=db,
    )

    service = EvidenceIntegrityService(db)

    return await service.get_history(
        evidence_id=evidence_id,
        skip=skip,
        limit=limit,
    )
