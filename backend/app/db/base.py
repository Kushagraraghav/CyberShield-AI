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
