"""Case management API endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import (
    require_analyst,
    require_viewer,
    require_case_viewer,
    require_case_analyst,
)
from app.db.session import get_db
from app.models.case import Case
from app.models.user import User
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst),
):
    """Create a new investigation case."""

    existing = db.scalar(
        select(Case).where(
            Case.case_number == case_data.case_number,
            Case.organization_id == case_data.organization_id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Case with this case number already exists in this organization",
        )

    case = Case(
        id=uuid4(),
        organization_id=case_data.organization_id,
        case_number=case_data.case_number,
        title=case_data.title,
        description=case_data.description,
        status=case_data.status,
        priority=case_data.priority,
        created_by=current_user.id,
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case


@router.get(
    "",
    response_model=list[CaseResponse],
)
def list_cases(
    organization_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_viewer),
):
    """List investigation cases."""

    if organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="organization_id is required",
        )

    query = (
        select(Case)
        .where(Case.organization_id == organization_id)
        .order_by(Case.created_at.desc())
    )

    cases = db.scalars(query).all()

    return list(cases)


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_viewer),
):
    """Get a case by ID."""

    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.patch(
    "/{case_id}",
    response_model=CaseResponse,
)
def update_case(
    case_id: UUID,
    case_data: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_analyst),
):
    """Update an investigation case."""

    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    update_data = case_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)

    return case


@router.delete(
    "/{case_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_case(
    case_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_case_analyst),
):
    """Delete an investigation case."""

    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    db.delete(case)
    db.commit()

    return None
