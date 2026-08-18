from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.evidence_analysis import (
    EvidenceAnalysisCreate,
    EvidenceAnalysisOut,
)
from app.services.evidence_analysis_service import EvidenceAnalysisService
from app.api.v1.dependencies import require_evidence_analyst, require_evidence_viewer
from app.models.user import User

router = APIRouter(
    prefix="/evidence-analysis",
    tags=["Evidence Analysis"],
)


@router.post(
    "",
    response_model=EvidenceAnalysisOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_evidence_analysis(
    payload: EvidenceAnalysisCreate,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Create a new evidence analysis record."""
    return await EvidenceAnalysisService.create_analysis(
        db=db,
        evidence_id=payload.evidence_id,
        organization_id=payload.organization_id,
        analysis_type=payload.analysis_type,
        analyzed_by=payload.analyzed_by,
        tool_used=payload.tool_used,
        analyst_notes=payload.analyst_notes,
    )


@router.get(
    "/{analysis_id}",
    response_model=EvidenceAnalysisOut,
)
async def get_evidence_analysis(
    analysis_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    """Get an evidence analysis within an organization."""
    analysis = await EvidenceAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        organization_id=organization_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence analysis not found",
        )

    return analysis


@router.get(
    "/evidence/{evidence_id}",
    response_model=list[EvidenceAnalysisOut],
)
async def list_evidence_analyses(
    evidence_id: UUID,
    organization_id: UUID,
    current_user: User = Depends(require_evidence_viewer),
    db: AsyncSession = Depends(get_db),
):
    """List all analyses for evidence within an organization."""
    return await EvidenceAnalysisService.list_evidence_analyses(
        db=db,
        evidence_id=evidence_id,
        organization_id=organization_id,
    )


@router.patch(
    "/{analysis_id}/start",
    response_model=EvidenceAnalysisOut,
)
async def start_evidence_analysis(
    analysis_id: UUID,
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Mark an evidence analysis as in progress."""
    analysis = await EvidenceAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        organization_id=organization_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence analysis not found",
        )

    return await EvidenceAnalysisService.start_analysis(db, analysis)


@router.patch(
    "/{analysis_id}/complete",
    response_model=EvidenceAnalysisOut,
)
async def complete_evidence_analysis(
    analysis_id: UUID,
    organization_id: UUID,
    findings: str | None = None,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Mark an evidence analysis as completed."""
    analysis = await EvidenceAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        organization_id=organization_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence analysis not found",
        )

    return await EvidenceAnalysisService.complete_analysis(
        db,
        analysis,
        findings,
    )


@router.patch(
    "/{analysis_id}/fail",
    response_model=EvidenceAnalysisOut,
)
async def fail_evidence_analysis(
    analysis_id: UUID,
    organization_id: UUID,
    findings: str | None = None,
    current_user: User = Depends(require_evidence_analyst),
    db: AsyncSession = Depends(get_db),
):
    """Mark an evidence analysis as failed."""
    analysis = await EvidenceAnalysisService.get_analysis(
        db=db,
        analysis_id=analysis_id,
        organization_id=organization_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence analysis not found",
        )

    return await EvidenceAnalysisService.fail_analysis(
        db,
        analysis,
        findings,
    )



