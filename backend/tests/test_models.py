"""Tests for database models."""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from app.models import (
    User, Organization, OrganizationMember, Case, Incident,
    Alert, Evidence, ThreatIndicator, AuditLog
)


def test_user_model_instantiation():
    """Test creating a User model instance."""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password_hash="hashed_password",
        is_active=True,
        is_superuser=False
    )
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.is_superuser is False


def test_organization_model_instantiation():
    """Test creating an Organization model instance."""
    org = Organization(
        name="Test Corp",
        description="A test organization",
        is_active=True
    )
    
    assert org.name == "Test Corp"
    assert org.description == "A test organization"
    assert org.is_active is True


def test_organization_member_model_instantiation():
    """Test creating an OrganizationMember model instance."""
    org_id = uuid4()
    user_id = uuid4()
    
    member = OrganizationMember(
        user_id=user_id,
        organization_id=org_id,
        role="analyst"
    )
    
    assert member.user_id == user_id
    assert member.organization_id == org_id
    assert member.role == "analyst"


def test_case_model_instantiation():
    """Test creating a Case model instance."""
    org_id = uuid4()
    
    case = Case(
        organization_id=org_id,
        case_number="CASE-001",
        title="Test Case",
        description="A test case",
        status="open",
        priority="high"
    )
    
    assert case.organization_id == org_id
    assert case.case_number == "CASE-001"
    assert case.title == "Test Case"
    assert case.status == "open"
    assert case.priority == "high"


def test_incident_model_instantiation():
    """Test creating an Incident model instance."""
    case_id = uuid4()
    org_id = uuid4()
    now = datetime.now(timezone.utc)
    
    incident = Incident(
        case_id=case_id,
        organization_id=org_id,
        title="Test Incident",
        description="A test incident",
        severity="critical",
        status="open",
        source="IDS",
        detected_at=now
    )
    
    assert incident.case_id == case_id
    assert incident.organization_id == org_id
    assert incident.severity == "critical"
    assert incident.status == "open"
    assert incident.detected_at == now


def test_alert_model_instantiation():
    """Test creating an Alert model instance."""
    org_id = uuid4()
    now = datetime.now(timezone.utc)
    
    alert = Alert(
        organization_id=org_id,
        title="Test Alert",
        description="A test alert",
        severity="high",
        status="new",
        source="Firewall",
        detected_at=now
    )
    
    assert alert.organization_id == org_id
    assert alert.title == "Test Alert"
    assert alert.severity == "high"
    assert alert.status == "new"
    assert alert.detected_at == now


def test_evidence_model_instantiation():
    """Test creating an Evidence model instance."""
    case_id = uuid4()
    org_id = uuid4()
    now = datetime.now(timezone.utc)
    
    evidence = Evidence(
        case_id=case_id,
        organization_id=org_id,
        evidence_number="EV-001",
        name="Disk Image",
        description="A forensic disk image",
        evidence_type="disk_image",
        file_name="drive.dd",
        file_size=1024000000,
        sha256_hash="a" * 64,
        collected_at=now
    )
    
    assert evidence.case_id == case_id
    assert evidence.organization_id == org_id
    assert evidence.evidence_number == "EV-001"
    assert evidence.evidence_type == "disk_image"
    assert evidence.file_size == 1024000000


def test_threat_indicator_model_instantiation():
    """Test creating a ThreatIndicator model instance."""
    org_id = uuid4()
    now = datetime.now(timezone.utc)
    
    indicator = ThreatIndicator(
        organization_id=org_id,
        indicator_type="ip",
        indicator_value="192.168.1.100",
        confidence=95,
        severity="high",
        source="Threat Feed",
        first_seen=now,
        is_active=True
    )
    
    assert indicator.organization_id == org_id
    assert indicator.indicator_type == "ip"
    assert indicator.indicator_value == "192.168.1.100"
    assert indicator.confidence == 95
    assert indicator.is_active is True


def test_audit_log_model_instantiation():
    """Test creating an AuditLog model instance."""
    org_id = uuid4()
    user_id = uuid4()
    
    audit_log = AuditLog(
        organization_id=org_id,
        user_id=user_id,
        action="create",
        resource_type="case",
        resource_id="case-123",
        ip_address="127.0.0.1",
        user_agent="Mozilla/5.0",
        details="Created a new case"
    )
    
    assert audit_log.organization_id == org_id
    assert audit_log.user_id == user_id
    assert audit_log.action == "create"
    assert audit_log.resource_type == "case"


def test_user_model_has_required_fields():
    """Test that User model has all required fields."""
    user_fields = {
        'id', 'email', 'username', 'full_name', 'password_hash',
        'is_active', 'is_superuser', 'created_at', 'updated_at'
    }
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password_hash="hashed",
        is_active=True,
        is_superuser=False
    )
    
    for field in user_fields:
        assert hasattr(user, field), f"User model missing field: {field}"


def test_organization_model_has_required_fields():
    """Test that Organization model has all required fields."""
    org_fields = {'id', 'name', 'description', 'is_active', 'created_at', 'updated_at'}
    org = Organization(
        name="Test Corp",
        description="Test",
        is_active=True
    )
    
    for field in org_fields:
        assert hasattr(org, field), f"Organization model missing field: {field}"


def test_case_model_has_required_fields():
    """Test that Case model has all required fields."""
    case_fields = {
        'id', 'organization_id', 'case_number', 'title', 'description',
        'status', 'priority', 'created_by', 'created_at', 'updated_at'
    }
    case = Case(
        organization_id=uuid4(),
        case_number="CASE-001",
        title="Test",
        status="open",
        priority="medium"
    )
    
    for field in case_fields:
        assert hasattr(case, field), f"Case model missing field: {field}"


def test_incident_model_has_required_fields():
    """Test that Incident model has all required fields."""
    incident_fields = {
        'id', 'case_id', 'organization_id', 'title', 'description',
        'severity', 'status', 'source', 'detected_at', 'resolved_at',
        'created_at', 'updated_at'
    }
    incident = Incident(
        case_id=uuid4(),
        organization_id=uuid4(),
        title="Test",
        severity="high",
        status="open",
        detected_at=datetime.now(timezone.utc)
    )
    
    for field in incident_fields:
        assert hasattr(incident, field), f"Incident model missing field: {field}"


def test_alert_model_has_required_fields():
    """Test that Alert model has all required fields."""
    alert_fields = {
        'id', 'organization_id', 'incident_id', 'title', 'description',
        'severity', 'status', 'source', 'source_event_id',
        'detected_at', 'acknowledged_at', 'resolved_at', 'created_at', 'updated_at'
    }
    alert = Alert(
        organization_id=uuid4(),
        title="Test",
        severity="high",
        status="new",
        source="Test",
        detected_at=datetime.now(timezone.utc)
    )
    
    for field in alert_fields:
        assert hasattr(alert, field), f"Alert model missing field: {field}"


def test_evidence_model_has_required_fields():
    """Test that Evidence model has all required fields."""
    evidence_fields = {
        'id', 'case_id', 'organization_id', 'evidence_number', 'name',
        'description', 'evidence_type', 'file_name', 'file_size',
        'sha256_hash', 'md5_hash', 'storage_path', 'collected_at',
        'collected_by', 'created_at'
    }
    evidence = Evidence(
        case_id=uuid4(),
        organization_id=uuid4(),
        evidence_number="EV-001",
        name="Test",
        evidence_type="disk_image",
        collected_at=datetime.now(timezone.utc)
    )
    
    for field in evidence_fields:
        assert hasattr(evidence, field), f"Evidence model missing field: {field}"


def test_threat_indicator_model_has_required_fields():
    """Test that ThreatIndicator model has all required fields."""
    ti_fields = {
        'id', 'organization_id', 'indicator_type', 'indicator_value',
        'confidence', 'severity', 'source', 'first_seen', 'last_seen',
        'is_active', 'created_at', 'updated_at'
    }
    indicator = ThreatIndicator(
        organization_id=uuid4(),
        indicator_type="ip",
        indicator_value="192.168.1.1",
        confidence=100,
        severity="high",
        first_seen=datetime.now(timezone.utc)
    )
    
    for field in ti_fields:
        assert hasattr(indicator, field), f"ThreatIndicator model missing field: {field}"


def test_audit_log_model_has_required_fields():
    """Test that AuditLog model has all required fields."""
    al_fields = {
        'id', 'organization_id', 'user_id', 'action', 'resource_type',
        'resource_id', 'ip_address', 'user_agent', 'details', 'created_at'
    }
    audit_log = AuditLog(
        action="create",
        resource_type="case"
    )
    
    for field in al_fields:
        assert hasattr(audit_log, field), f"AuditLog model missing field: {field}"


def test_organization_member_model_has_required_fields():
    """Test that OrganizationMember model has all required fields."""
    om_fields = {'id', 'user_id', 'organization_id', 'role', 'created_at'}
    member = OrganizationMember(
        user_id=uuid4(),
        organization_id=uuid4(),
        role="analyst"
    )
    
    for field in om_fields:
        assert hasattr(member, field), f"OrganizationMember model missing field: {field}"


def test_case_status_values():
    """Test that Case model supports expected status values."""
    valid_statuses = ["open", "investigating", "closed", "archived"]
    
    for status in valid_statuses:
        case = Case(
            organization_id=uuid4(),
            case_number="TEST",
            title="Test",
            status=status,
            priority="medium"
        )
        assert case.status == status


def test_alert_status_values():
    """Test that Alert model supports expected status values."""
    valid_statuses = ["new", "acknowledged", "investigating", "resolved", "dismissed"]
    
    for status in valid_statuses:
        alert = Alert(
            organization_id=uuid4(),
            title="Test",
            severity="high",
            status=status,
            source="Test",
            detected_at=datetime.now(timezone.utc)
        )
        assert alert.status == status
