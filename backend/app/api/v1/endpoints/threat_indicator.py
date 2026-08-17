"""Threat Indicator API endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.dependencies import (
    require_indicator_analyst,
    require_indicator_org_analyst,
    require_indicator_org_viewer,
    require_indicator_viewer,
)
from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.threat_indicator import ThreatIndicator
from app.models.user import User
from app.schemas.threat_indicator import (
    ThreatIndicatorCreate,
    ThreatIndicatorResponse,
    ThreatIndicatorUpdate,
)

router = APIRouter(
    prefix="/threat-indicators",
    tags=["Threat Indicators"],
)


@router.post(
    "",
    response_model=ThreatIndicatorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_threat_indicator(
    indicator_data: ThreatIndicatorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new threat indicator."""

    # Only admin/analyst of the specified organization
    # can create an indicator.
    require_indicator_org_analyst(
        organization_id=indicator_data.organization_id,
        current_user=current_user,
        db=db,
    )

    indicator = ThreatIndicator(
        id=uuid4(),
        organization_id=indicator_data.organization_id,
        indicator_type=indicator_data.indicator_type,
        indicator_value=indicator_data.indicator_value,
        confidence=indicator_data.confidence,
        severity=indicator_data.severity,
        source=indicator_data.source,
        first_seen=indicator_data.first_seen,
    )

    db.add(indicator)
    db.commit()
    db.refresh(indicator)

    return indicator


@router.get(
    "",
    response_model=list[ThreatIndicatorResponse],
)
def list_threat_indicators(
    organization_id: UUID,
    indicator_type: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List threat indicators for an organization."""

    # Organization isolation:
    # user must belong to this organization.
    require_indicator_org_viewer(
        organization_id=organization_id,
        current_user=current_user,
        db=db,
    )

    query = select(ThreatIndicator).where(
        ThreatIndicator.organization_id == organization_id
    )

    if indicator_type is not None:
        query = query.where(
            ThreatIndicator.indicator_type == indicator_type
        )

    if is_active is not None:
        query = query.where(
            ThreatIndicator.is_active == is_active
        )

    query = query.order_by(
        ThreatIndicator.created_at.desc()
    )

    return list(db.scalars(query).all())


@router.get(
    "/search",
    response_model=list[ThreatIndicatorResponse],
)
def search_threat_indicators(
    organization_id: UUID,
    search_term: str | None = None,
    indicator_type: str | None = None,
    severity: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search threat indicators within an organization."""

    require_indicator_org_viewer(
        organization_id=organization_id,
        current_user=current_user,
        db=db,
    )

    query = select(ThreatIndicator).where(
        ThreatIndicator.organization_id == organization_id
    )

    if search_term:
        query = query.where(
            ThreatIndicator.indicator_value.ilike(f"%{search_term}%")
        )

    if indicator_type is not None:
        query = query.where(
            ThreatIndicator.indicator_type == indicator_type
        )

    if severity is not None:
        query = query.where(
            ThreatIndicator.severity == severity
        )

    if is_active is not None:
        query = query.where(
            ThreatIndicator.is_active == is_active
        )

    query = query.order_by(
        ThreatIndicator.created_at.desc()
    )

    return list(db.scalars(query).all())


@router.get(
    "/{indicator_id}/correlations",
)
def correlate_threat_indicator(
    indicator_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Find malware analyses containing this threat indicator."""

    require_indicator_viewer(
        indicator_id=indicator_id,
        current_user=current_user,
        db=db,
    )

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    from app.models.malware_analysis import MalwareAnalysis
    import json

    analyses = db.scalars(
        select(MalwareAnalysis).where(
            MalwareAnalysis.organization_id
            == indicator.organization_id,
            MalwareAnalysis.status == "completed",
        )
    ).all()

    correlations = []

    for analysis in analyses:
        if not analysis.extracted_indicators:
            continue

        try:
            extracted = json.loads(
                analysis.extracted_indicators
            )
        except (json.JSONDecodeError, TypeError):
            continue

        matched = False
        matched_locations = []

        for key in ["ips", "domains", "urls"]:
            values = extracted.get(key, [])

            if indicator.indicator_value in values:
                matched = True
                matched_locations.append(key)

        if indicator.indicator_type == "hash":
            static_data = {}

            if analysis.static_analysis:
                try:
                    static_data = json.loads(
                        analysis.static_analysis
                    )
                except (json.JSONDecodeError, TypeError):
                    pass

            hashes = static_data.get("hashes", {})

            if indicator.indicator_value in hashes.values():
                matched = True
                matched_locations.append("hashes")

        if matched:
            correlations.append(
                {
                    "analysis_id": str(analysis.id),
                    "sample_id": str(analysis.sample_id),
                    "organization_id": str(
                        analysis.organization_id
                    ),
                    "status": analysis.status,
                    "analysis_type": analysis.analysis_type,
                    "threat_classification": (
                        analysis.threat_classification
                    ),
                    "severity": analysis.severity,
                    "risk_score": analysis.risk_score,
                    "analysis_engine": analysis.analysis_engine,
                    "matched_locations": matched_locations,
                    "analyzed_at": (
                        analysis.analyzed_at
                    ),
                }
            )

    return {
        "indicator": {
            "id": str(indicator.id),
            "type": indicator.indicator_type,
            "value": indicator.indicator_value,
        },
        "correlation_count": len(correlations),
        "correlations": correlations,
    }


@router.get(
    "/{indicator_id}",
    response_model=ThreatIndicatorResponse,
)
def get_threat_indicator(
    indicator_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a threat indicator by ID."""

    # Organization isolation is checked through the
    # indicator itself.
    require_indicator_viewer(
        indicator_id=indicator_id,
        current_user=current_user,
        db=db,
    )

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    return indicator


@router.patch(
    "/{indicator_id}",
    response_model=ThreatIndicatorResponse,
)
def update_threat_indicator(
    indicator_id: UUID,
    indicator_data: ThreatIndicatorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a threat indicator."""

    # Only admin/analyst in the indicator's organization
    # can update it.
    require_indicator_analyst(
        indicator_id=indicator_id,
        current_user=current_user,
        db=db,
    )

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    update_data = indicator_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(indicator, field, value)

    db.commit()
    db.refresh(indicator)

    return indicator


@router.delete(
    "/{indicator_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_threat_indicator(
    indicator_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a threat indicator."""

    # Only admin/analyst in the indicator's organization
    # can delete it.
    require_indicator_analyst(
        indicator_id=indicator_id,
        current_user=current_user,
        db=db,
    )

    indicator = db.get(ThreatIndicator, indicator_id)

    if indicator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat indicator not found",
        )

    db.delete(indicator)
    db.commit()

    return None