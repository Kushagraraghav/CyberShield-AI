from pathlib import Path
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_case_analyst, require_case_viewer, require_evidence_viewer, require_evidence_analyst
from app.db.session import get_db
from app.models.evidence import Evidence
from app.models.user import User
from app.utils.file_storage import save_evidence_file
from app.utils.file_hash import calculate_file_hashes

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
async def create_evidence(
    case_id: UUID,
    organization_id: UUID = Form(...),
    evidence_number: str = Form(...),
    name: str = Form(...),
    evidence_type: str = Form(...),
    collected_at: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_analyst),
):
    """Create an evidence record from an uploaded file."""

    existing = db.scalar(
        select(Evidence).where(
            Evidence.evidence_number == evidence_number
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Evidence with this evidence number already exists",
        )

    evidence_id = uuid4()

    storage_path, file_size = await save_evidence_file(
        file=file,
        organization_id=organization_id,
        evidence_id=evidence_id,
    )

    sha256_hash, md5_hash = calculate_file_hashes(storage_path)

    evidence = Evidence(
        id=evidence_id,
        case_id=case_id,
        organization_id=organization_id,
        evidence_number=evidence_number,
        name=name,
        description=description,
        evidence_type=evidence_type,
        file_name=file.filename,
        file_size=file_size,
        sha256_hash=sha256_hash,
        md5_hash=md5_hash,
        storage_path=str(storage_path),
        collected_at=collected_at,
        collected_by=current_user.id,
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
    current_user: User = Depends(require_evidence_viewer),
):
    """List evidence."""

    if case_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="case_id is required",
        )

    query = (
        select(Evidence)
        .where(Evidence.case_id == case_id)
        .order_by(Evidence.created_at.desc())
    )

    if organization_id is not None:
        query = query.where(
            Evidence.organization_id == organization_id
        )

    evidence = db.scalars(query).all()

    return list(evidence)


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
    """Delete evidence and its stored file."""

    evidence = db.get(Evidence, evidence_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence not found",
        )

    # Delete physical file first.
    if evidence.storage_path:
        file_path = Path(evidence.storage_path)

        if file_path.exists():
            file_path.unlink()

    # Delete database record.
    db.delete(evidence)
    db.commit()

    return None
