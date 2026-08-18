"""SQLAlchemy declarative base for models."""

from sqlalchemy.orm import declarative_base

# Declarative base for all models
Base = declarative_base()

# Import all models to register them with Alembic
# This must be done after Base is created to avoid circular imports
from app.models.user import User  # noqa: F401, E402
from app.models.organization import Organization  # noqa: F401, E402
from app.models.organization_member import OrganizationMember  # noqa: F401, E402
from app.models.case import Case  # noqa: F401, E402
from app.models.incident import Incident  # noqa: F401, E402
from app.models.alert import Alert  # noqa: F401, E402
from app.models.evidence import Evidence  # noqa: F401, E402
from app.models.threat_indicator import ThreatIndicator  # noqa: F401, E402
from app.models.audit_log import AuditLog  # noqa: F401, E402
from app.models.malware_sample import MalwareSample  # noqa: F401, E402



from app.models.malware_analysis import MalwareAnalysis  # noqa: F401, E402

from app.models.threat_intelligence_feed import ThreatIntelligenceFeed  # noqa: F401, E402


from app.models.evidence_custody import EvidenceCustody  # noqa: F401, E402

from app.models.evidence_integrity import EvidenceIntegrityVerification  # noqa: F401, E402

from app.models.forensic_timeline_event import ForensicTimelineEvent  # noqa: F401, E402
