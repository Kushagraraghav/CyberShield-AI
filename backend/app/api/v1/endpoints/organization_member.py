"""Organization membership API endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import (
    require_organization_member_admin,
    require_organization_member_viewer,
)
from app.db.session import get_db
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.user import User
from app.schemas.organization_member import (
    OrganizationMemberCreate,
    OrganizationMemberResponse,
    OrganizationMemberUpdate,
)

router = APIRouter(
    prefix="/organization-members",
    tags=["Organization Members"],
)


@router.post(
    "",
    response_model=OrganizationMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization_member(
    data: OrganizationMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organization_member_admin),
):
    """Add a user to an organization."""

    user = db.get(User, data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    organization = db.get(Organization, data.organization_id)

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    existing = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.user_id == data.user_id,
            OrganizationMember.organization_id == data.organization_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this organization",
        )

    member = OrganizationMember(
        id=uuid4(),
        user_id=data.user_id,
        organization_id=data.organization_id,
        role=data.role,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get(
    "",
    response_model=list[OrganizationMemberResponse],
)
def list_organization_members(
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organization_member_viewer),
):
    """List organization memberships."""

    query = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id
    )

    return query.order_by(
        OrganizationMember.created_at.desc()
    ).all()


@router.get(
    "/{member_id}",
    response_model=OrganizationMemberResponse,
)
def get_organization_member(
    member_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organization_member_viewer),
):
    """Get a specific organization membership."""

    member = db.get(OrganizationMember, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization membership not found",
        )

    return member


@router.patch(
    "/{member_id}",
    response_model=OrganizationMemberResponse,
)
def update_organization_member(
    member_id: UUID,
    data: OrganizationMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organization_member_admin),
):
    """Update an organization member's role."""

    member = db.get(OrganizationMember, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization membership not found",
        )

    member.role = data.role

    db.commit()
    db.refresh(member)

    return member


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization_member(
    member_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_organization_member_admin),
):
    """Remove a user from an organization."""

    member = db.get(OrganizationMember, member_id)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization membership not found",
        )

    db.delete(member)
    db.commit()

    return None
