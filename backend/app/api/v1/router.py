"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.organization import router as organization_router
from app.api.v1.endpoints.organization_member import (
    router as organization_member_router,
)
from app.api.v1.endpoints.case import router as case_router
from app.api.v1.endpoints.incident import router as incident_router
from app.api.v1.endpoints.alert import router as alert_router
from app.api.v1.endpoints.evidence import router as evidence_router
from app.api.v1.endpoints.threat_indicator import router as threat_indicator_router
from app.api.v1.endpoints.audit_log import router as audit_log_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.malware import router as malware_router
from app.api.v1.endpoints.threat_intelligence_feed import router as threat_intelligence_feed_router


router = APIRouter(prefix="/api/v1")

# Core endpoints
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(organization_router)
router.include_router(organization_member_router)
router.include_router(case_router)
router.include_router(incident_router)
router.include_router(alert_router)
router.include_router(evidence_router)

# Security / forensic endpoints
router.include_router(threat_indicator_router)
router.include_router(audit_log_router)
router.include_router(user_router)
router.include_router(malware_router)
router.include_router(threat_intelligence_feed_router)

from app.api.v1.endpoints.malware_analysis import router as malware_analysis_router
router.include_router(malware_analysis_router)

