"""Evidence API endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_case_analyst, require_case_viewer, require_evidence_viewer, require_evidence_analyst
from app.db.session import get_db
from app.models.evidence import Evidence
from app.models.user import User
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceDetailResponse,
    EvidenceResponse,
    EvidenceUpdate,
)

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.post(
    "",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evidence(
    evidence_data: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_analyst),
):
    """Create a new evidence record."""

    existing = db.scalar(
        select(Evidence).where(
            Evidence.evidence_number == evidence_data.evidence_number
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Evidence with this evidence number already exists",
        )

    evidence = Evidence(
        id=uuid4(),
        case_id=evidence_data.case_id,
        organization_id=evidence_data.organization_id,
        evidence_number=evidence_data.evidence_number,
        name=evidence_data.name,
        description=evidence_data.description,
        evidence_type=evidence_data.evidence_type,
        file_name=evidence_data.file_name,
        file_size=evidence_data.file_size,
        sha256_hash=evidence_data.sha256_hash,
        md5_hash=evidence_data.md5_hash,
        storage_path=evidence_data.storage_path,
        collected_at=evidence_data.collected_at,
        collected_by=evidence_data.collected_by,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence


@router.get(
    "",
    response_model=list[EvidenceResponse],
)
def list_evidence(
    organization_id: UUID | None = None,
    case_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_viewer),
):
    """List evidence records."""

    if organization_id is None and case_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="organization_id or case_id is required",
        )

    query = select(Evidence).order_by(Evidence.created_at.desc())

    if organization_id:
        query = query.where(Evidence.organization_id == organization_id)

    if case_id:
        query = query.where(Evidence.case_id == case_id)

    evidence_records = db.scalars(query).all()

    return list(evidence_records)


@router.get(
    "/{evidence_id}",
    response_model=EvidenceDetailResponse,
)
def get_evidence(
    evidence_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_evidence_viewer),
):
    """Get evidence by ID."""

    evidence = db.get(Evidence, evidence_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    return evidence


@router.patch(
    "/{evidence_id}",
    response_model=EvidenceResponse,
)
def update_evidence(
    evidence_id: UUID,
    evidence_data: EvidenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_evidence_analyst),
):
    """Update evidence."""

    evidence = db.get(Evidence, evidence_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    update_data = evidence_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(evidence, field, value)

    db.commit()
    db.refresh(evidence)

    return evidence


@router.delete(
    "/{evidence_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_evidence(
    evidence_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_evidence_analyst),
):
    """Delete evidence."""

    evidence = db.get(Evidence, evidence_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    db.delete(evidence)
    db.commit()

    return None